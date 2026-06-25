---
name: visa-entry
description: >
  Researches visa and entry requirements by passport nationality and destination.
  Use for 签证, visa, ESTA, eTA, Schengen, 入境, passport validity, or border entry questions.
license: MIT
compatibility: Requires web access for official verification. Reference data may become outdated.
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Visa & Entry

Visa and entry analysis for international trips. **Policies change — always note query date and link official sources.**

## Inputs

| Required | Optional |
|----------|----------|
| Passport nationality | Second passport / residency |
| Destination country | Transit countries |
| Stay length | Purpose (tourism/business) |
| Travel dates | Existing visas |

## Workflow

1. Read [references/visa-quick-ref.md](references/visa-quick-ref.md) for quick routing
2. **Verify** via official sources (immigration site, embassy, IATA Travel Centre)
3. Output structured summary (see template below)

## Output Template

```
结论: [visa-free / visa on arrival / visa required / eTA or ESTA]
类型: [...]
办理时长: [...] · 建议提前 [...] 天
费用: [...]
材料: 护照 / 照片 / 行程 / 保险 / 资金证明 ...
限制: 护照≥6个月、空白页、返程票 ...
官方链接: [URL]
查询日期: YYYY-MM-DD
```

## Universal Rules

- Passport valid ≥6 months at entry (most countries)
- ≥2 blank visa pages
- Schengen: 90/180 day rule
- US ESTA / Canada eTA / UK ETA where applicable
- Transit may still require a visa

## Pitfalls

- Never assert visa-free from memory alone
- PRC / HKSAR / MAC / TWN passports differ — confirm which passport
- Visa on arrival ≠ visa-free

## Related

- [travel-documents](../travel-documents/SKILL.md) — checklists
- [references/visa-quick-ref.md](references/visa-quick-ref.md)
