---
name: dietary-global
description: >
  Customizes meal plans for dietary restrictions worldwide (halal, vegan, gluten-free,
  allergies, no spicy food). Use when the user mentions 不吃辣, 清真, 素食, allergy, or food restrictions.
license: MIT
metadata:
  atlas:
    version: "1.1.0"
    parent: atlas-agent
---

# Dietary Global

Meal planning with global dietary restrictions. Every meal must include **restaurant + dishes + tags + price**.

## Tags

| Tag | Meaning |
|-----|---------|
| 🟢 | Safe for user's restrictions |
| 🟡 | Can be modified on request |
| 🔴 | Contains restricted ingredients |
| ⚠️ | Cross-contamination risk |

## Playbook

See [references/dietary-playbooks.md](references/dietary-playbooks.md) for:

- Key phrases by language (no spice, vegetarian, gluten-free, nut allergy)
- Region tips (Sichuan, Thailand, India, Japan, Italy, US)
- Halal / vegan / celiac guidance

## Output Format (required)

```
[餐次] — [餐厅]（[区域]）
- [菜名] 🟢 ¥XXX — [note]
人均：XXX [local] ≈ XXX [user currency]
```

## Pitfalls

- "Not spicy" means different things by culture — give local phrases
- Severe allergies: recommend allergy cards; avoid high cross-contamination street food
