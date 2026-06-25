#!/usr/bin/env python3
"""Frankfurter (ECB) currency client for AtlasAgent. No API key required.

Usage:
  python3 currency_client.py rates --base USD
  python3 currency_client.py convert 1000 --from USD --to JPY
  python3 currency_client.py convert 500 --from EUR --to CNY --to GBP
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import List, Optional

BASE_URL = "https://api.frankfurter.app"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "AtlasAgent/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def cmd_rates(base: str, targets: Optional[List[str]]) -> None:
    params = {"from": base.upper()}
    if targets:
        params["to"] = ",".join(t.upper() for t in targets)
    url = f"{BASE_URL}/latest?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    print(f"📅 汇率日期: {data['date']}")
    print(f"💱 基准: {data['base']}")
    for cur, rate in sorted(data.get("rates", {}).items()):
        print(f"  1 {data['base']} = {rate:.4f} {cur}")


def cmd_convert(amount: float, src: str, targets: List[str]) -> None:
    src = src.upper()
    tgt = ",".join(t.upper() for t in targets)
    url = f"{BASE_URL}/latest?amount={amount}&from={src}&to={tgt}"
    data = fetch_json(url)
    print(f"📅 汇率日期: {data['date']}")
    print(f"💰 {amount:,.2f} {src} =")
    for cur, val in sorted(data.get("rates", {}).items()):
        print(f"   {val:,.2f} {cur}")


def main():
    p = argparse.ArgumentParser(description="AtlasAgent currency client (Frankfurter/ECB)")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("rates", help="Show exchange rates")
    r.add_argument("--base", default="USD")
    r.add_argument("--to", nargs="*", help="Target currencies")

    c = sub.add_parser("convert", help="Convert amount")
    c.add_argument("amount", type=float)
    c.add_argument("--from", dest="src", required=True)
    c.add_argument("--to", nargs="+", required=True)

    args = p.parse_args()
    if args.cmd == "rates":
        cmd_rates(args.base, args.to)
    elif args.cmd == "convert":
        cmd_convert(args.amount, args.src, args.to)


if __name__ == "__main__":
    main()
