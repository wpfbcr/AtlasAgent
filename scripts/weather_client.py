#!/usr/bin/env python3
"""Date-aware Open-Meteo forecasts and current conditions. No API key."""
import argparse
from datetime import date, datetime, timedelta, timezone
import json
import math
import sys
import urllib.parse
from zoneinfo import ZoneInfo

from http_client import APIError, fetch_json

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
DAILY_FIELDS = "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max"
WMO_CODES = {0: "晴", 1: "大部晴朗", 2: "局部多云", 3: "多云", 45: "雾", 48: "雾凇", 51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨", 56: "冻毛毛雨", 57: "强冻毛毛雨", 61: "小雨", 63: "中雨", 65: "大雨", 66: "冻雨", 67: "强冻雨", 71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒", 80: "小阵雨", 81: "阵雨", 82: "大阵雨", 85: "阵雪", 86: "强阵雪", 95: "雷暴", 96: "雷暴伴冰雹", 99: "雷暴伴大冰雹"}


def geocode(city, country=None):
    params = {"name": city, "count": 10, "language": "en", "format": "json"}
    if country:
        params["countryCode"] = country.upper()
    results = fetch_json(GEOCODE_URL + "?" + urllib.parse.urlencode(params)).get("results") or []
    if not isinstance(results, list) or any(not isinstance(r, dict) for r in results):
        raise APIError("Malformed geocoding results")
    for result in results:
        if any(not isinstance(result.get(key), (int, float)) or not math.isfinite(result[key]) for key in ("latitude", "longitude")):
            raise APIError("Geocoding result is missing coordinates")
    if country:
        results = [r for r in results if r.get("country_code", "").upper() == country.upper()]
    exact = [r for r in results if r.get("name", "").casefold() == city.casefold()]
    results = exact or results
    # Deduplicate aliases for the same coordinates, without guessing between towns.
    results = list({(r["latitude"], r["longitude"]): r for r in results}.values())
    if not results:
        raise ValueError("City not found: " + city)
    if len(results) != 1:
        choices = "; ".join("{}, {}, {} ({},{})".format(r.get("name"), r.get("admin1", ""), r.get("country", ""), r["latitude"], r["longitude"]) for r in results)
        raise ValueError("Ambiguous city; specify --country or --lat/--lon: " + choices)
    r = results[0]
    return {"name": r.get("name", city), "country": r.get("country", ""), "lat": r["latitude"], "lon": r["longitude"], "timezone": r.get("timezone") or "UTC"}


def local_today(tz):
    return datetime.now(ZoneInfo(tz) if tz != "auto" else timezone.utc).date()


def forecast(lat, lon, days, timezone="auto", start=None, today=None):
    if not 1 <= days <= 16:
        raise ValueError("--days must be between 1 and 16; longer trips need climate reference, not a forecast")
    today = today or local_today(timezone)
    start = start or today
    end = start + timedelta(days=days - 1)
    if start < today or end > today + timedelta(days=15):
        raise ValueError("Requested dates {} to {} are outside the forecast window {} to {}; use climate reference and recheck near departure".format(start, end, today, today + timedelta(days=15)))
    params = {"latitude": lat, "longitude": lon, "daily": DAILY_FIELDS, "timezone": timezone, "start_date": start.isoformat(), "end_date": end.isoformat()}
    data = fetch_json(FORECAST_URL + "?" + urllib.parse.urlencode(params))
    expected = [(start + timedelta(days=i)).isoformat() for i in range(days)]
    if not isinstance(data.get("daily"), dict) or data["daily"].get("time") != expected:
        raise APIError("Forecast date coverage does not match requested dates")
    return data


def current(lat, lon, timezone="auto"):
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,weather_code,precipitation,wind_speed_10m", "timezone": timezone}
    data = fetch_json(FORECAST_URL + "?" + urllib.parse.urlencode(params))
    if not isinstance(data.get("current"), dict) or not data["current"].get("time"):
        raise APIError("Service did not return current conditions with a timestamp")
    return data


def value_at(daily, key, index):
    values = daily.get(key) or []
    if not isinstance(values, list):
        return None
    return values[index] if index < len(values) else None


def fmt(value, suffix="", digits=0):
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return "暂无数据"
    return ("{:." + str(digits) + "f}").format(value) + suffix


def print_forecast(loc, data):
    daily = data.get("daily", {})
    print("地点: {}, {} | 时区: {}".format(loc["name"], loc.get("country", ""), data.get("timezone", loc.get("timezone"))))
    print("日期 | 天气 | 最高 | 最低 | 降水mm | 降水概率 | 风速km/h")
    for i, d in enumerate(daily.get("time", [])):
        code = value_at(daily, "weather_code", i)
        cells = [d, WMO_CODES.get(code, "暂无数据" if code is None else "code=" + str(code)), fmt(value_at(daily, "temperature_2m_max", i), "°C"), fmt(value_at(daily, "temperature_2m_min", i), "°C"), fmt(value_at(daily, "precipitation_sum", i), digits=1), fmt(value_at(daily, "precipitation_probability_max", i), "%"), fmt(value_at(daily, "wind_speed_10m_max", i))]
        print(" | ".join(cells))


def iso_date(text):
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use a valid YYYY-MM-DD date") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("forecast", "current"):
        child = sub.add_parser(name)
        child.add_argument("--city")
        child.add_argument("--country", help="ISO two-letter country code")
        child.add_argument("--lat", type=float)
        child.add_argument("--lon", type=float)
        child.add_argument("--timezone", help="IANA timezone (recommended for coordinates)")
        child.add_argument("--json", action="store_true")
        if name == "forecast":
            child.add_argument("--from", dest="start", type=iso_date, help="First trip date, YYYY-MM-DD")
            child.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    try:
        if args.cmd == "forecast" and not 1 <= args.days <= 16:
            raise ValueError("--days must be between 1 and 16")
        if args.country and (len(args.country) != 2 or not args.country.isalpha()):
            raise ValueError("--country must be a two-letter country code")
        if args.city and (args.lat is not None or args.lon is not None):
            raise ValueError("Choose --city or --lat/--lon")
        if args.city:
            loc = geocode(args.city, args.country)
        elif args.lat is not None and args.lon is not None:
            if not math.isfinite(args.lat) or not math.isfinite(args.lon) or not -90 <= args.lat <= 90 or not -180 <= args.lon <= 180:
                raise ValueError("Latitude/longitude are out of range")
            loc = {"name": "{},{}".format(args.lat, args.lon), "country": "", "lat": args.lat, "lon": args.lon, "timezone": "auto"}
        else:
            raise ValueError("Provide --city or both --lat and --lon")
        if args.timezone:
            ZoneInfo(args.timezone)
            loc["timezone"] = args.timezone
        data = forecast(loc["lat"], loc["lon"], args.days, loc["timezone"], args.start) if args.cmd == "forecast" else current(loc["lat"], loc["lon"], loc["timezone"])
        if args.json:
            print(json.dumps({"status": "ok", "location": loc, args.cmd: data}, ensure_ascii=False, indent=2))
        elif args.cmd == "forecast":
            print_forecast(loc, data)
        else:
            now = data["current"]
            print("{} | {} ({}) | {} | {}".format(loc["name"], now["time"], data.get("timezone", loc["timezone"]), WMO_CODES.get(now.get("weather_code"), "暂无数据"), fmt(now.get("temperature_2m"), "°C", 1)))
    except (APIError, ValueError, KeyError, OverflowError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        else:
            print("Weather error: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
