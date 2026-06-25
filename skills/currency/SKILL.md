---
name: currency
description: >
  Converts travel budgets across currencies using Frankfurter/ECB rates (no API key).
  Use when estimating trip costs, comparing plans, 汇率, 预算, or multi-currency prices.
license: MIT
compatibility: Requires Python 3.9+ and network access. Requires ATLAS_ROOT repo clone.
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Currency

Multi-currency conversion for travel budgets.

## Setup

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
export ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
```

## Commands

```bash
python3 "$ATLAS_SCRIPTS/currency_client.py" rates --base USD
python3 "$ATLAS_SCRIPTS/currency_client.py" rates --base EUR --to JPY CNY GBP
python3 "$ATLAS_SCRIPTS/currency_client.py" convert 8000 --from CNY --to JPY EUR
```

## Rules

- Budget tables show **local currency + user currency**
- Always note `汇率日期: YYYY-MM-DD`
- Airport/hotel FX rates are worse than ECB reference — mention in cautions

## Common Codes

USD, EUR, GBP, JPY, CNY, AUD, THB, KRW, CHF, SGD

## Verify

```bash
python3 "$ATLAS_SCRIPTS/currency_client.py" convert 100 --from USD --to JPY
```
