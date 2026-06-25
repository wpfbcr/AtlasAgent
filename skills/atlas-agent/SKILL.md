---
name: atlas-agent
description: >
  Plans global travel itineraries with multi-plan comparison, day-by-day schedules,
  multi-currency budgets, visa/diet/transport guidance, and PDF export.
  Use when the user asks for trip planning, vacation itinerary, travel guide,
  行程规划, 旅游攻略, or holiday planning for any destination worldwide.
license: MIT
compatibility: Requires Python 3.9+, network access, and the full AtlasAgent repo (set ATLAS_ROOT).
metadata:
  atlas:
    version: "1.1.0"
    related: [weather, currency, visa-entry, dietary-global, transport-global, local-intel, travel-documents, budget-optimizer]
---

# AtlasAgent — Global Travel Planning

Orchestrates worldwide trip planning: multi-plan comparison, daily schedules, budgets, visa/diet/transport decisions, PDF export.

## When to Use

- User provides origin, dates, party size — needs an itinerary
- User wants destination recommendations with plan comparison
- User has booked flights/hotels and needs a concrete schedule
- Multi-city or cross-timezone trips

## Required Inputs

Ask for missing fields before planning:

| Required | Optional |
|----------|----------|
| Origin (city + country) | Budget (total or per person + currency) |
| Dates + duration | Style (food, nature, history, urban, adventure, family, romantic) |
| Party size + relationship | Mobility/diet/photo/slow-travel preferences |
| Destination (or ask agent to suggest) | Passport nationality, booked tickets/hotels |
| | Output language (default: 中文 if user writes in Chinese) |

## Paths (required)

**Install the full repository** — `skills/` alone is not enough.

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
export ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
export ATLAS_REF="$ATLAS_ROOT/skills/atlas-agent/references"
```

Install: see [docs/install.md](../../docs/install.md) or run `bash scripts/install.sh`.

## Workflow

### Phase 0 — Profile

1. Passport nationality → read `visa-entry` skill
2. Dietary restrictions → read `dietary-global` skill
3. Booked tickets/hotels → treat as **fixed anchors**

### Phase 1 — Data (parallel)

```bash
# Weather
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city "<city>" --days <N>

# Currency
python3 "$ATLAS_SCRIPTS/currency_client.py" rates --base <currency>
python3 "$ATLAS_SCRIPTS/currency_client.py" convert <amount> --from <A> --to <B>

# Calendar
python3 "$ATLAS_SCRIPTS/holiday_check.py" --city "<city>" --from YYYY-MM-DD --days <N>
```

**Geography** (first available):

1. `$MAPS_SCRIPT` if set (any geocoder/POI CLI, e.g. OpenStreetMap client)
2. Web search + `$ATLAS_REF/destinations/<city>.md`
3. Never invent hotel/restaurant names

**Flights/hotels (optional L1):** trvl MCP or web search — see [mcp/recommended-servers.md](../../mcp/recommended-servers.md)

**Reviews (optional L1):** `local-intel` skill

### Phase 1.5 — Disambiguation

Do not guess ambiguous names. Present options and **ask the user to choose**:

- Location, transport, duration, ticket/booking needs
- Local + English names

Examples: Paris (France vs Texas), Springfield (30+ US cities).

### Phase 2 — Scheduling

1. Use `holiday_check.py` — weekdays, holidays, museum closure hints
2. Book major sights on **weekdays** when possible
3. Arrival day = half day; allow jet-lag buffer after eastbound flights
4. Multi-city: minimize backtracking (use distance/routing tools if available)
5. Respect booked transport times as hard constraints

### Phase 3 — Itinerary

Each plan includes:

- Round-trip transport (route, time, price in local + user currency)
- Weather summary (Open-Meteo)
- Visa/entry summary (from visa-entry)
- One-line trip theme + destination timezone

**Daily table:**

| | Schedule | Stay |
|---|---|---|
| D1 date (weekday) | AM → PM → evening (hours) | area/hotel |
| … | … | … |

**Required sections:** must-eat list, 2–3 stays, budget table (budget-optimizer), transport decision (transport-global), document checklist (travel-documents), cautions.

**Meals:** every meal = restaurant + dishes with dietary tags (🟢🟡🔴⚠️) + price per person.

**Pace:** only one "intense" day; others relaxed. Mark activity hours.

Comparison rubric: [references/comparison-rubric.md](references/comparison-rubric.md)

### Phase 4 — Compare & Recommend

Multi-plan table (days, budget, travel time, romance/food/photo/culture/family stars, effort, visa complexity). End with 1–2 sentence ranking.

### Phase 5 — Export

```bash
python3 "$ATLAS_SCRIPTS/md2pdf.py" itinerary.md
```

## Capability Tiers

| Tier | Sources | Label in output |
|------|---------|-----------------|
| L0 | Scripts + `$ATLAS_REF/destinations/` | Default |
| L1 | + trvl MCP, social research | Cite source + query time |
| L2 | + Amadeus, calendar/docs export | Cite API + query time |

If data is estimated, say: **「基于 reference 估算，出行前请验证」**.

## Companion Skills

| Skill | Purpose |
|-------|---------|
| `weather` | Forecasts |
| `currency` | FX conversion |
| `visa-entry` | Visa/entry |
| `dietary-global` | Diet restrictions |
| `transport-global` | Transport choices |
| `local-intel` | UGC research |
| `travel-documents` | Checklists |
| `budget-optimizer` | Budget format |

## Pitfalls

- Rate-limit POI APIs (>2s between calls); fall back to references
- Visa/policy: always note query date; re-check before departure
- FX: note rate date (Frankfurter/ECB)
- Southern hemisphere seasons invert vs northern
- Tipping varies by country → budget-optimizer
- Never recommend conflicting transport if user already booked

## Verify

```bash
python3 "$ATLAS_SCRIPTS/weather_client.py" forecast --city Paris --days 3
python3 "$ATLAS_SCRIPTS/currency_client.py" convert 100 --from EUR --to CNY
python3 "$ATLAS_SCRIPTS/holiday_check.py" --city Paris --from 2026-07-14 --days 5
```
