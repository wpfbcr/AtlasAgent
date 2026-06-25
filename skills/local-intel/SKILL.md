---
name: local-intel
description: >
  Researches destination reputation from Reddit, YouTube, and web UGC to find real tips and traps.
  Use for 避坑, local tips, overrated sights, or validating tourist attractions.
license: MIT
compatibility: Requires web search or social research tools (e.g. Agent-Reach).
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Local Intel

Supplement official/reference data with community sentiment.

## Sources

Use any available research tool:

- Web search: `site:reddit.com [city] itinerary`, `tourist trap`, `best time to visit`
- YouTube travel vlogs (note publish date; watch for sponsorships)
- Twitter/X, local forums

If [Agent-Reach](https://github.com/Panniantong/Agent-Reach) is installed, follow its routing for Reddit/YouTube.

## Search Templates

| Goal | Query pattern |
|------|----------------|
| Itinerary ideas | `reddit [destination] [N] days itinerary` |
| Restaurant traps | `reddit [city] restaurant tourist trap` |
| Season | `reddit best time visit [destination]` |
| Crowds | `reddit [city] [month] crowds closure` |

## Output

```
口碑摘要 — [destination]
高频推荐（≥3 sources）: ...
高频避坑: ...
争议点: ...
信息时效: latest source YYYY-MM
来源: [URLs]
```

## Rules

- Prefer posts within 12 months
- Cross-check before removing a sight from itinerary
- Marketing/spam: new accounts pushing one venue = suspicious
- Does not replace official hours/visa data
