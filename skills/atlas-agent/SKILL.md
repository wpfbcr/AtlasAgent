---
name: atlas-agent
description: "全球高级定制化旅游攻略：多方案对比、逐日行程、多币种预算、签证/饮食/交通决策、PDF导出。适用于 Hermes/Cursor/Claude 等 Agent。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [travel, planning, itinerary, global, budget, visa, worldwide]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [weather, currency, visa-entry, dietary-global, transport-global, local-intel, travel-documents, budget-optimizer, maps]
    supersedes: [travel-planning]
---

# AtlasAgent — 全球旅游规划主编排器

为全球任意出发地/目的地生成高级定制化行程：多方案对比、逐日安排、多币种预算、签证提醒、饮食/交通/节奏定制，支持 PDF 导出。

**替代** 旧版 `travel-planning`（中国境内专用），面向全世界用户。

## When to Use

- 用户提供出发地、日期、天数、人数，需要行程规划
- 用户不确定目的地，需要推荐 + 多方案对比
- 用户已有目的地或已订票，需要落地到具体行程
- 跨国/跨时区/多城市联游

## Required Inputs

从用户处收集（缺失则用 `clarify` 追问）：

| 必填 | 选填 |
|------|------|
| 出发地（城市 + 国家） | 预算范围（总额或人均，含币种） |
| 日期 + 天数 | 风格偏好（美食/自然/历史/都市/冒险/亲子/浪漫） |
| 人数 + 关系 | 特殊需求（不爬山/轮椅/拍照/慢节奏） |
| 目的地（或让 Agent 推荐） | 护照国籍、饮食限制、已订机票/酒店 |
| 输出语言偏好 | 偏好币种（默认按用户 locale） |

## AtlasAgent Root

```bash
ATLAS=~/AtlasAgent   # 或 git clone 后的实际路径
SCRIPTS=$ATLAS/scripts
REF=$ATLAS/references
```

## Planning Workflow

### Phase 0: Profile & Constraints

1. 确认用户**国籍/护照** → 调用 `visa-entry` skill
2. 确认**饮食限制** → 调用 `dietary-global` skill
3. 确认**输出语言**（默认中文；国际用户可英文/双语）
4. 若用户已订票/酒店 → 以已预订时间为**不可移动锚点**

### Phase 1: Data Gathering（并行）

```bash
# 1. 地理（依赖 Hermes maps skill 或 AtlasAgent 同目录 maps）
MAPS=~/.hermes/skills/productivity/maps/scripts/maps_client.py
python3 $MAPS search "<目的地>"
python3 $MAPS timezone <lat> <lon>
python3 $MAPS nearby --near "<地标>" --category hotel --limit 10
python3 $MAPS nearby --near "<地标>" --category restaurant --limit 10

# 2. 天气（AtlasAgent weather skill）
python3 $SCRIPTS/weather_client.py forecast --city "<城市>" --days <N>

# 3. 汇率（AtlasAgent currency skill）
python3 $SCRIPTS/currency_client.py rates --base <用户币种>
python3 $SCRIPTS/currency_client.py convert <金额> --from <A> --to <B>

# 4. 目的地知识库（优先本地 reference，再 web_search）
# 读取 $REF/destinations/<city>.md

# 5. 交通/航班（L0: web_search + reference；L1: trvl MCP，见 mcp/recommended-servers.md）

# 6. 口碑调研（L1: local-intel skill → Reddit/YouTube）
```

**并行原则**：地理 + 天气 + 汇率 + 知识库同时拉取；航班/酒店限流时降级到 reference 估算并标注「需实时验证」。

### Phase 1.5: Ambiguity Resolution

全球地名/景区常有歧义。**不要猜测**，用 `clarify()` 列出选项：

- 位置、交通方式、预计耗时、门票/预约要求
- 中英文/当地语言名称对照

示例：`Paris` → 法国巴黎 vs 美国德州 Paris；`Springfield` → 美国有 30+ 个同名城市。

### Phase 2: Schedule Engineering

1. **验证日历**：`python3 $SCRIPTS/holiday_check.py --city "<城市>" --from YYYY-MM-DD --days N`
   - 确认每天星期几
   - 标记当地公共假日、博物馆闭馆日（周一闭馆：卢浮宫、大英博物馆等）
   - 热门景点（迪士尼、卢浮宫、故宫类）优先排**工作日**
2. **跨时区处理**：
   - 长途航班抵达日 = **抵达半日**，不排高强度行程
   - Jet lag 缓冲：东行航班后 Day1 只安排轻松活动
3. **多城市顺序**：用 `maps distance` 优化路线，避免折返
4. **已订票锚点**：以航班/火车时间为硬约束，向前/向后推算

### Phase 3: Itinerary Construction

每个方案包含：

```
✈️/🚄 往返交通：路线 + 时间 + 单价（原币种 + 用户币种）+ 总价
🌤️ 天气概况（Open-Meteo 7 日预报摘要）
🛂 签证/入境提醒（visa-entry 输出摘要）
🎯 风格定位：一句话概括
🕐 时区：目的地 UTC 偏移
```

**逐日行程表**：

| | 行程安排 | 住宿 |
|---|---|---|
| D1 日期（周X） | 上午→下午→晚上（标注时长 h） | 区域/酒店 |
| D2 ... | ... | ... |
| Dn | 上午→下午→返程 | - |

**附加模块**（每个方案必须有）：

- 🍜 **必吃清单**：5–8 项（含 dietary-global 辣度/过敏标签 🟢🟡🔴⚠️）
- 🏨 **推荐住宿**：2–3 家（优先 maps 真实 POI + 价格区间）
- 💰 **预算估算表**（budget-optimizer 格式，多币种）
- 🚗/🚇 **交通决策摘要**（transport-global）
- 📋 **证件/保险清单**（travel-documents）
- ⚠️ **注意事项**：天气穿着、小费文化、预订提醒、避坑

**逐顿点菜规则**：每一顿饭必须给出 **餐厅名 + 推荐菜（含饮食标签）+ 人均价格（双币种）**。

**节奏控制**（全程仅 1 天「紧」）：

```
Day1  ████░░░░  抵达/Jet lag → 松
Day2  ████████  主攻日         → 紧
Day3  █████░░░  户外/远郊      → 舒
Day4  ███░░░░░  慢收尾+返程    → 缓
```

### Phase 4: Comparison & Recommendation

对比表格（参见 `references/comparison-rubric.md`）：

| 维度 | 方案A | 方案B | ... |
|------|-------|-------|-----|
| 天数 | | | |
| 人均预算（用户币种） | | | |
| 飞行/铁路时间 | | | |
| 浪漫指数 ⭐×5 | | | |
| 美食指数 ⭐×5 | | | |
| 出片指数 ⭐×5 | | | |
| 文化深度 ⭐×5 | | | |
| 亲子友好 ⭐×5 | | | |
| 体力消耗 | 低/中/高 | | |
| 签证复杂度 | 低/中/高 | | |
| 特色体验 | | | |

最后 **1–2 句推荐排序** + 选择理由。

### Phase 5: Export

```bash
# Markdown → PDF（中文/多语言字体）
python3 $SCRIPTS/md2pdf.py <行程.md>

# 可选导出（Related Skills）
# - obsidian：保存为 vault 笔记
# - notion：结构化数据库
# - google-workspace：Calendar 事件 + Sheets 预算
```

## Three-Tier Capability Model

| 层级 | 数据源 | 标注要求 |
|------|--------|----------|
| L0 零配置 | maps + Open-Meteo + Frankfurter + references | 默认模式 |
| L1 增强 | + trvl MCP + local-intel | 标注实时价格来源 |
| L2 专业 | + Amadeus + OAuth 导出 | 标注 API 来源与查询时间 |

**禁止虚构**：酒店/餐厅优先 maps 真实 POI；API 失败时标注「基于 reference 估算，出行前请验证」。

## Related Skills（本仓库内）

| Skill | 用途 |
|-------|------|
| `weather` | Open-Meteo 预报 |
| `currency` | 多币种换算 |
| `visa-entry` | 签证/入境 |
| `dietary-global` | 饮食限制 |
| `transport-global` | 交通方式决策 |
| `local-intel` | 口碑调研 |
| `travel-documents` | 证件清单 |
| `budget-optimizer` | 预算优化 |

## External Dependencies

| 依赖 | 用途 | 必需 |
|------|------|------|
| Hermes `maps` | geocode / POI / 路线 / 时区 | L0 强烈推荐 |
| `fpdf2` | PDF 导出 | 可选 |
| trvl MCP | 航班/酒店实时搜索 | L1 可选 |
| agent-reach | Reddit/YouTube 调研 | L1 可选 |

## Pitfalls

- **Overpass 429**：maps `nearby` 间隔 >2s；失败用 `$REF/destinations/`
- **OSRM SSL 失败**：用直线距离 + reference 交通时间
- **Open-Meteo 限流**：免费无 Key，极少 429；失败用 reference 气候表
- **签证信息时效性**：必须标注查询日期，建议出发前 30 天再核实
- **汇率波动**：预算表标注汇率日期与来源（Frankfurter/ECB）
- **南半球季节**：6 月 = 悉尼冬季，勿按北半球打包
- **小费文化**：美国 18–20%、日本无小费、欧洲因国而异 → 纳入 budget-optimizer
- **星期/假日**：必须用 `holiday_check.py` 验证，不可凭记忆
- **已订票**：不得推荐冲突航班/车次

## Verification

```bash
python3 $SCRIPTS/weather_client.py forecast --city "Paris" --days 3
python3 $SCRIPTS/currency_client.py convert 100 --from EUR --to CNY
python3 $SCRIPTS/holiday_check.py --city "Paris" --from 2026-07-14 --days 5
python3 $MAPS search "Eiffel Tower"
```

## Output Language

默认**中文输出**；用户指定英文或其他语言时全文切换，仅保留地名/代码/API 原文。
