---
name: dietary-global
description: "全球饮食限制定制：清真/素食/无麸质/过敏/不吃辣，逐道菜标注 🟢🟡🔴⚠️。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [dietary, food, halal, vegan, allergy, travel]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [atlas-agent]
---

# Dietary Global Skill

为全球任意目的地定制饮食方案，确保每一顿饭有**餐厅 + 推荐菜 + 饮食标签 + 人均价格**。

## When to Use

- 用户有饮食限制（不吃辣/清真/素食/纯素/无麸质/海鲜过敏/坚果过敏等）
- 目的地饮食文化与用户习惯差异大（川渝/印度/中东/日本）
- 需要逐顿点菜推荐

## Dietary Tags

| 标签 | 含义 |
|------|------|
| 🟢 | 安全 — 符合用户所有限制 |
| 🟡 | 需注意 — 可要求调整（如「去辣」「无坚果」） |
| 🔴 | 避免 — 含用户禁忌成分 |
| ⚠️ | 交叉污染风险 — 共用厨房/炸锅（无麸质/严重过敏） |

## Restriction Playbooks

详见 `references/dietary-playbooks.md`。摘要：

### 不吃辣（川渝湘泰等）

- 教用户当地语言的关键句（见 playbooks）
- 中国：「一点辣椒都不要，清汤/白味」
- 泰国：「mai phet」（不要辣）
- 印度：指定 North Indian 不辣菜（Dal Tadka、Naan、Raita）

### 清真 Halal

- 优先 Halal 认证餐厅或穆斯林聚集区
- 日本/韩国 Halal 选择有限，标注具体区域（东京：浅草/新大久保）

### 素食 / 纯素 Vegan

- 印度：最易（40%+ 素食选项）
- 日本：困难（出汁含鱼），标注 shojin ryori 寺庙料理
- 欧洲：V 标记常见，纯素需确认无奶酪/黄油

### 无麸质 Gluten-Free

- 意大利：风险高（共用厨房），选 dedicated GF 餐厅
- 美国/英国：GF 标签较规范

### 过敏 Allergy

- 严重过敏（花生/贝类）：准备 allergy card（多语言），见 playbooks
- 日本：8 大过敏原标注法较完善

## Output Rules（强制）

每一顿饭格式：

```
🍽️ [早/午/晚] — [餐厅名]（[区域]）
- [菜名] 🟢 ¥XXX / $XX — [一句话说明]
- [菜名] 🟡 — 备注：可要求去辣/去坚果
人均：XXX [当地币种] ≈ XXX [用户币种]
```

**禁止**只给餐厅名不给菜。

## Integration

`atlas-agent` Phase 0 收集饮食限制 → Phase 3 逐顿输出带标签菜单。

## Pitfalls

- 「不辣」在不同文化含义不同，必须给当地语言关键句
- 过敏用户避免 street food（交叉污染）
- 宗教饮食（清真/犹太洁食）需 clarify 严格程度
