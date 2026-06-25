---
name: visa-entry
description: "签证与入境要求：护照有效期、免签/落地签/电子签、ESTA/eTA 等，含 web 核实流程。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [visa, passport, entry, immigration, travel]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [atlas-agent, travel-documents]
---

# Visa & Entry Skill

为全球行程提供签证/入境要求分析。**政策变动频繁，必须标注查询日期并建议出发前 30 天再核实。**

## When to Use

- 用户国籍/护照与目的地不同国
- 跨国联游涉及中转国签证
- 需要 ESTA / eTA / ETA / EVW 等电子旅行授权

## Required Inputs

| 必填 | 选填 |
|------|------|
| 护照国籍 | 第二国籍/永居 |
| 目的地国家 | 中转国 |
| 停留天数 | 旅行目的（旅游/商务） |
| 出发日期 | 已有签证类型 |

## Workflow

### Step 1: Reference 快速判断

读取 `references/visa-quick-ref.md` 获取常见路线速查（中国/美国/欧盟/英国/日本/澳洲护照 × 热门目的地）。

### Step 2: Web 核实（必须）

并行搜索官方来源（优先级从高到低）：

1. 目的地国家移民局/外交部官网
2. IATA Travel Centre（timatic 类信息）
3. 用户护照国驻外使领馆签证页

```bash
# 用 web_search 或 browser 工具查询，示例关键词：
# "China passport visa Japan 2026 tourist"
# "US ESTA requirements 2026"
```

### Step 3: 输出结构

```
🛂 签证结论：[免签 / 落地签 / 需提前办签 / 需电子旅行授权]
📋 类型：[旅游签 / ESTA / eTA / Schengen C visa / ...]
⏱️ 办理时长：[X 个工作日] + 建议提前 [Y] 天申请
💰 费用：[金额 + 币种]
📄 材料清单：护照 / 照片 / 行程单 / 保险 / 银行流水 ...
⚠️ 特别限制：护照有效期 ≥6 个月、空白页、返程机票、资金证明
🔗 官方链接：[URL]
📅 信息查询日期：YYYY-MM-DD
```

## Universal Rules（全球通用）

| 规则 | 说明 |
|------|------|
| 护照有效期 | 多数国家要求入境时护照剩余 ≥6 个月 |
| 空白页 | 至少 2 页空白签证页 |
|  Schengen 区 | 90/180 天规则，按首次入境日计算 |
| 美国 ESTA | 38 个免签国公民需 ESTA（$21，2 年有效） |
| 加拿大 eTA | 免签国公民需 eTA（CAD $7） |
| 英国 ETA | 2025 起逐步对免签国实施 |
| 澳大利亚 ETA/eVisitor | 视国籍不同 |
| 中转签证 | 即使不出机场，部分国家仍需过境签 |

## Multi-Country Trips

联游时逐国列出签证要求，并检查：
- 单次入境 vs 多次入境签证
- 申根区内外切换
- 美国 CBP 过境规则

## Pitfalls

- **绝不凭记忆断言免签** — 政策每年变化
- 台湾/港澳/大陆护照规则不同，必须 clarify 护照类型
- 落地签 ≠ 免签，需备现金/照片/返程票
- 电子签网站钓鱼多，只给官方链接
- 标注「本信息仅供参考，以官方为准」

## Related

- `travel-documents` — 护照/保险/紧急联系清单
- `atlas-agent` Phase 0 调用本 skill
