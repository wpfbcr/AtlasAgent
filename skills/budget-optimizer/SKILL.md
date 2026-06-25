---
name: budget-optimizer
description: >
  Formats and optimizes multi-currency travel budgets with tipping and hidden costs.
  Use when comparing plan costs, 预算, budget breakdown, or saving money on a trip.
license: MIT
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Budget Optimizer

Standard budget tables for atlas-agent plans.

## Setup

Use `currency` skill for FX. Note rate date on every table.

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
python3 "$ATLAS_ROOT/scripts/currency_client.py" convert <amount> --from <A> --to <B>
```

## Table Template

```
预算 — [plan name]
汇率日期: YYYY-MM-DD · 人数: N · 天数: D

| 项目 | 当地货币 | 用户货币 | 备注 |
|------|----------|----------|------|
| 国际/城际交通 | | | 含行李 |
| 住宿 (N-1 晚) | | | 档位说明 |
| 餐饮 | | | 含小费 |
| 门票/活动 | | | |
| 市内交通 | | | |
| 签证/保险 | | | 一次性 |
| 应急 buffer 10% | | | |
| 合计 / 人均 | | | |
```

## Tipping (include where relevant)

| Region | Guide |
|--------|-------|
| USA | 18–20% restaurants |
| Japan | No tipping |
| France | Service included; small change OK |
| UK | 10–12.5% |
| Thailand | ~10% |

## Hidden Costs Checklist

- Budget airline baggage
- City congestion/ERP fees
- US resort fees + tax
- Attraction timed-entry surcharges
- eSIM cost

## If Over Budget

1. Lower hotel tier (largest lever)
2. Shoulder season dates
3. Rail pass vs singles / budget airlines
4. Mix free sights + few paid highlights

## Pitfalls

- Use ranges when prices are uncertain — label as estimates
- Child/senior ticket discounts when applicable
