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
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city "Tokyo" --days 7
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --lat 48.8566 --lon 2.3522 --days 5
python3 "$ATLAS_SCRIPTS/weather_client.py" current --city "Paris"
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city "Sydney" --days 10 --json
```

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
