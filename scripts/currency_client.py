#!/usr/bin/env python3
"""Frankfurter currency CLI. Repeated --to values are combined."""
import argparse
from datetime import date
import json
import math
import re
import sys
import urllib.parse
from http_client import APIError, fetch_json

BASE_URL = "https://api.frankfurter.app"


def currency_code(text):
    text = text.upper()
    if not re.fullmatch(r"[A-Z]{3}", text):
        raise argparse.ArgumentTypeError("Currency must be a three-letter ISO code")
    return text


def conversion(amount, src, targets, round_results=True):
    if not math.isfinite(amount) or amount < 0:
        raise ValueError("Amount must be finite and non-negative")
    targets = list(dict.fromkeys(targets))
    foreign = [t for t in targets if t != src]
    # Get unit rates so zero amounts and same-currency conversions work locally.
    data = fetch_json(BASE_URL + "/latest?" + urllib.parse.urlencode({"from": src, "to": ",".join(foreign)})) if foreign else {"date": None, "base": src, "rates": {}}
    rates = data.get("rates", {})
    if not isinstance(rates, dict):
        raise APIError("Malformed exchange-rate response")
    if foreign and (not data.get("date") or data.get("base") != src):
        raise APIError("Missing or mismatched exchange-rate metadata")
    if data.get("date"):
        try:
            date.fromisoformat(data["date"])
        except (ValueError, TypeError) as exc:
            raise APIError("Invalid exchange-rate date") from exc
    result = {}
    for target in targets:
        rate = 1 if target == src else rates.get(target)
        if not isinstance(rate, (int, float)) or not math.isfinite(rate) or rate <= 0:
            raise APIError("Missing or invalid exchange rate for " + target)
        value = amount * rate
        if not math.isfinite(value):
            raise ValueError("Converted amount is too large")
        result[target] = round(value, 2) if round_results else value
    return {"date": data.get("date"), "base": src, "amount": amount, "rates": result, "source": "Frankfurter/ECB" if foreign else "identity (no FX needed)"}


def cmd_rates(base, targets, as_json=False):
    if targets:
        data = conversion(1, base.upper(), [t.upper() for t in targets], round_results=False)
    else:
        data = fetch_json(BASE_URL + "/latest?" + urllib.parse.urlencode({"from": base.upper()}))
        if not data.get("date") or data.get("base") != base.upper() or not isinstance(data.get("rates"), dict) or not data["rates"]:
            raise APIError("Missing exchange-rate data")
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("汇率日期: {} | 基准: {}".format(data.get("date") or "无需换汇", data.get("base", base)))
        for cur, rate in sorted(data["rates"].items()):
            print("1 {} = {:.4f} {}".format(base, rate, cur))


def cmd_convert(amount, src, targets, as_json=False):
    data = conversion(amount, src.upper(), [t.upper() for t in targets])
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("汇率日期: {}".format(data["date"] or "无需换汇"))
        print("{:,.2f} {} =".format(amount, data["base"]))
        for cur, value in sorted(data["rates"].items()):
            print("  {:,.2f} {}".format(value, cur))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rates")
    r.add_argument("--base", type=currency_code, default="USD")
    r.add_argument("--to", type=currency_code, nargs="+", action="extend")
    c = sub.add_parser("convert")
    c.add_argument("amount", type=float)
    c.add_argument("--from", dest="src", type=currency_code, required=True)
    c.add_argument("--to", type=currency_code, nargs="+", action="extend", required=True)
    for child in (r, c):
        child.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        if args.cmd == "rates":
            cmd_rates(args.base, args.to, args.json)
        else:
            cmd_convert(args.amount, args.src, args.to, args.json)
    except (APIError, ValueError, KeyError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        else:
            print("Currency error: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
