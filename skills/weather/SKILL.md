---
name: weather
description: >
  Fetches global weather forecasts via Open-Meteo without an API key.
  Use when planning travel dates, packing, outdoor activities, or when the user asks
  about weather, 天气, forecast, or climate at a destination.
license: MIT
compatibility: Requires Python 3.9+ and network access. Requires ATLAS_ROOT repo clone.
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Weather

Open-Meteo forecasts for travel planning (replaces wttr.in — more reliable globally).

## Setup

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
export ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
```

## Commands

```bash
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city "Tokyo" --country JP --days 7
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --lat 48.8566 --lon 2.3522 --days 5
python3 "$ATLAS_SCRIPTS/weather_client.py" current --city "Paris" --country FR
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city "Sydney" --country AU --days 10 --json
```

For travel dates, include `--from YYYY-MM-DD` and the exact number of trip days. The client rejects ranges outside the next 16 local dates instead of substituting today's forecast. For ambiguous city names, specify coordinates and `--timezone` after confirming the location; the client prints candidate locations instead of selecting the first.

`current` returns current conditions and their timestamp. `--json` is available for both commands. Missing observations appear as `暂无数据` in text; service failures have a nonzero exit code and an explicit error.

## Output Use

- Summarize in itinerary weather section
- Rain → swap outdoor sights for indoor backups
- Extreme heat/cold → packing notes
- Forecast beyond 7 days = trend only

## Pitfalls

- Southern hemisphere seasons differ (June in Sydney = winter)
- Mountain/coastal microclimates may differ from city forecast

## Verify

```bash
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city Paris --days 3
```
