---
name: transport-global
description: >
  Chooses transport modes for trips: metro vs rental car, rail passes, budget airlines, ferries.
  Use when the user asks 租车, rail pass, JR Pass, Eurail, or how to get around a destination.
license: MIT
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Transport Global

Structured transport decisions for global travel.

## Framework

For each question, output a 3-row comparison:

| Dimension | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| City mobility | | | |
| Day trips / intercity | | | |
| Total N-day cost | | | |

## Rules (summary)

See [references/transport-guides.md](references/transport-guides.md).

- **Strong metro cities** (Tokyo, Paris, London, NYC, Singapore): do not rent a car in city center
- **US/AU/NZ spread-out regions**: car often required
- **Europe multi-country**: compare Eurail pass vs point-to-point tickets
- **Japan**: recalculate JR Pass vs individual shinkansen fares post-2023 price hike
- **Deserts / remote**: guided tour or charter, not inexperienced self-drive

## Optional L1

Real-time prices via trvl MCP — [mcp/recommended-servers.md](../../mcp/recommended-servers.md)

## Pitfalls

- Left vs right-hand drive by country
- IDP requirements vary
- London/SG congestion charges, US resort fees — include in budget
