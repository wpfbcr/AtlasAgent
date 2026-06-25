#!/usr/bin/env python3
"""Calendar helper for AtlasAgent itinerary scheduling.

Validates weekday, flags common museum closure patterns, and lists dates.

Usage:
  python3 holiday_check.py --city "Paris" --from 2026-07-14 --days 7
  python3 holiday_check.py --from 2026-12-24 --days 5 --json
"""

import argparse
import json
from datetime import date, timedelta
from typing import Dict, List, Optional, Any

WEEKDAY_ZH = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# Common weekly closures (heuristic — agent must verify for specific venues)
CITY_CLOSURE_HINTS = {
    "paris": "卢浮宫/奥赛博物馆通常周二或周一闭馆，出发前查官网",
    "london": "大英博物馆通常无固定闭馆日；部分画廊周一闭馆",
    "rome": "梵蒂冈博物馆周日闭馆（除特殊开放日）",
    "tokyo": "多数博物馆周一闭馆",
    "new york": "部分博物馆周一或周二闭馆",
    "beijing": "故宫周一闭馆（法定节假日除外）",
}

# Fixed global travel peaks (planning hints, not exhaustive holiday DB)
GLOBAL_PEAKS = {
    (12, 24): "🎄 圣诞前夕 — 欧美机票/酒店涨价",
    (12, 25): "🎄 圣诞节 — 多数欧美景点特殊开放时间",
    (12, 31): "🎆 跨年 — 热门城市拥挤",
    (1, 1): "🎆 元旦 — 部分商店/餐厅休息",
    (2, 14): "💝 情人节 — 浪漫目的地餐厅需预约",
    (7, 14): "🇫🇷 法国国庆日（巴士底日）",
    (10, 1): "🇨🇳 中国国庆黄金周",
    (5, 1): "🌍 多国劳动节",
}


def analyze(start: date, days: int, city: Optional[str]) -> Dict[str, Any]:
    rows: List[dict] = []
    city_key = (city or "").lower().strip()
    hint = None
    for k, v in CITY_CLOSURE_HINTS.items():
        if k in city_key:
            hint = v
            break

    for i in range(days):
        d = start + timedelta(days=i)
        wd = d.weekday()
        is_weekend = wd >= 5
        peak = GLOBAL_PEAKS.get((d.month, d.day))
        notes = []
        if is_weekend:
            notes.append("⚠️ 周末 — 热门景点人流大，优先安排轻松/预约制景点")
        if peak:
            notes.append(peak)
        if i == 0:
            notes.append("📍 行程 Day1")
        rows.append({
            "date": d.isoformat(),
            "weekday": WEEKDAY_ZH[wd],
            "weekday_num": wd + 1,
            "is_weekend": is_weekend,
            "day_label": f"D{i + 1}",
            "notes": notes,
        })

    return {"city_hint": hint, "days": rows}


def main():
    p = argparse.ArgumentParser(description="AtlasAgent calendar checker")
    p.add_argument("--city", help="Destination city for closure hints")
    p.add_argument("--from", dest="start", required=True, help="Start date YYYY-MM-DD")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    start = date.fromisoformat(args.start)
    result = analyze(start, args.days, args.city)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if result["city_hint"]:
        print(f"🏛️ {args.city}: {result['city_hint']}")
        print()
    print(f"{'日期':<12} {'星期':<6} {'标签':<6} 备注")
    print("-" * 50)
    for row in result["days"]:
        tag = "周末" if row["is_weekend"] else "工作日"
        notes = "; ".join(row["notes"]) if row["notes"] else "-"
        print(f"{row['date']:<12} {row['weekday']:<6} {tag:<6} {row['day_label']} {notes}")


if __name__ == "__main__":
    main()
