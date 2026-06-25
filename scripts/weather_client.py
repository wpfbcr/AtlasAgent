#!/usr/bin/env python3
"""Open-Meteo weather client for AtlasAgent. No API key required.

Usage:
  python3 weather_client.py forecast --city "Tokyo" --days 7
  python3 weather_client.py forecast --lat 35.6762 --lon 139.6503 --days 5
  python3 weather_client.py current --city "Paris"
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "AtlasAgent/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def geocode(city: str) -> dict:
    params = urllib.parse.urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    data = fetch_json(f"{GEOCODE_URL}?{params}")
    results = data.get("results") or []
    if not results:
        raise SystemExit(f"City not found: {city}")
    r = results[0]
    return {
        "name": r.get("name"),
        "country": r.get("country"),
        "lat": r["latitude"],
        "lon": r["longitude"],
        "timezone": r.get("timezone", "UTC"),
    }


def forecast(lat: float, lon: float, days: int, timezone: str = "auto") -> dict:
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
        "timezone": timezone,
        "forecast_days": min(days, 16),
    })
    return fetch_json(f"{FORECAST_URL}?{params}")


WMO_CODES = {
    0: "晴", 1: "大部晴朗", 2: "局部多云", 3: "多云",
    45: "雾", 48: "雾凇", 51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨", 71: "小雪", 73: "中雪", 75: "大雪",
    80: "小阵雨", 81: "阵雨", 82: "大阵雨", 95: "雷暴", 96: "雷暴+小冰雹", 99: "雷暴+大冰雹",
}


def print_forecast(loc: dict, data: dict) -> None:
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    print(f"📍 {loc['name']}, {loc.get('country', '')} ({loc['lat']:.2f}, {loc['lon']:.2f})")
    print(f"🕐 Timezone: {data.get('timezone', loc.get('timezone'))}")
    print()
    print(f"{'日期':<12} {'天气':<10} {'最高':>6} {'最低':>6} {'降水mm':>8} {'降水%':>6} {'风速km/h':>10}")
    print("-" * 62)
    for i, d in enumerate(dates):
        code = daily.get("weather_code", [0])[i]
        wx = WMO_CODES.get(code, f"code={code}")
        tmax = daily.get("temperature_2m_max", [None])[i]
        tmin = daily.get("temperature_2m_min", [None])[i]
        precip = daily.get("precipitation_sum", [0])[i]
        prob = daily.get("precipitation_probability_max", [None])[i]
        wind = daily.get("wind_speed_10m_max", [None])[i]
        prob_s = f"{prob}%" if prob is not None else "-"
        print(f"{d:<12} {wx:<10} {tmax:>5.0f}°C {tmin:>5.0f}°C {precip:>7.1f} {prob_s:>6} {wind:>9.0f}")


def main():
    p = argparse.ArgumentParser(description="AtlasAgent Open-Meteo weather client")
    sub = p.add_subparsers(dest="cmd", required=True)

    fc = sub.add_parser("forecast", help="Daily forecast")
    fc.add_argument("--city", help="City name for geocoding")
    fc.add_argument("--lat", type=float)
    fc.add_argument("--lon", type=float)
    fc.add_argument("--days", type=int, default=7)
    fc.add_argument("--json", action="store_true")

    cur = sub.add_parser("current", help="Current conditions summary")
    cur.add_argument("--city", required=True)

    args = p.parse_args()

    if args.cmd == "forecast":
        if args.city:
            loc = geocode(args.city)
        elif args.lat is not None and args.lon is not None:
            loc = {"name": f"{args.lat},{args.lon}", "country": "", "lat": args.lat, "lon": args.lon, "timezone": "auto"}
        else:
            raise SystemExit("Provide --city or --lat/--lon")
        data = forecast(loc["lat"], loc["lon"], args.days, loc.get("timezone", "auto"))
        if args.json:
            print(json.dumps({"location": loc, "forecast": data}, ensure_ascii=False, indent=2))
        else:
            print_forecast(loc, data)

    elif args.cmd == "current":
        loc = geocode(args.city)
        data = forecast(loc["lat"], loc["lon"], 1, loc.get("timezone", "auto"))
        daily = data.get("daily", {})
        d0 = daily.get("time", ["?"])[0]
        code = daily.get("weather_code", [0])[0]
        tmax = daily.get("temperature_2m_max", [None])[0]
        tmin = daily.get("temperature_2m_min", [None])[0]
        print(f"📍 {loc['name']}, {loc['country']}")
        print(f"📅 {d0}: {WMO_CODES.get(code, code)}, {tmin:.0f}–{tmax:.0f}°C")


if __name__ == "__main__":
    main()
