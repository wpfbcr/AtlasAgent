---
name: transport-global
description: "全球交通决策：租车/铁路通票/地铁/廉航/包车/渡轮，按目的地给出三维对比与决策规则。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [transport, car-rental, rail-pass, flights, travel]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [atlas-agent, budget-optimizer]
---

# Transport Global Skill

当用户问「要不要租车 / 买铁路通票 / 怎么在城市间移动」时，按目的地特征给出结构化决策。

## When to Use

- 市内交通方式选择
- 城际/跨国交通（火车 vs 飞机 vs 自驾）
- 租车 vs 公共交通成本对比
- 特殊地形（沙漠/岛屿/阿尔卑斯）

## Decision Framework

### 三维对比表（每个方案必须输出）

| 维度 | 方案A | 方案B | 谁赢 |
|------|-------|-------|------|
| 市区出行 | | | |
| 远郊/跨城 | | | |
| N天总成本 | | | |

## Regional Rules

详见 `references/transport-guides.md`。核心规则：

### 地铁发达城市 → 不租车

**适用**：东京、巴黎、伦敦、纽约、新加坡、香港、首尔、巴塞罗那

| 维度 | 🚗 租车 | 🚇 公共交通 | 谁赢 |
|------|---------|------------|------|
| 市区 | 停车贵+难找 | 覆盖全部景点 | 地铁 |
| 远郊 | 灵活 | 火车+打车 | 平手 |
| 总成本 | 高 | 低 | 地铁 |

### 欧洲铁路通票

- **Eurail Global Pass**：多国联游 3 国以上可能划算
- **各国 Pass**：瑞士 Travel Pass、日本 JR Pass（需提前算单买 vs Pass）
- 规则：用 maps `distance` + web_search 查点对点票价对比

### 美国/澳洲/新西兰 → 常需租车

景点分散、公共交通弱。例外：纽约曼哈顿、旧金山市区。

### 岛屿/环线

- 冰岛 Ring Road → 租车或跟团
- 夏威夷 → 每岛租车
- 冲绳 → 租车或公交（有限）

### 沙漠/草原

- 中卫、撒哈拉、蒙古 → **包车**，不建议无经验自驾

### 廉航策略

- 欧洲：Ryanair/EasyJet + 严格行李限制，算隐性成本
- 东南亚：AirAsia/Lion Air，注意安全记录

### 日本特殊

- JR Pass 2023 涨价后需逐段计算
- 市内：Suica/Pasmo + 地铁
- 远郊：新干线单买可能更便宜

## L1 增强：trvl MCP

配置见 `mcp/recommended-servers.md`，可查询实时航班/火车/租车价格。

## Integration

`atlas-agent` Phase 3 输出「🚗/🚇 交通决策摘要」，引用本 skill 结论。

## Pitfalls

- 左舵/右舵国家切换（英国/日本/澳洲 vs 大陆/美国）
- 国际驾照（IDP）要求因国而异
- 伦敦/新加坡 congestion charge / ERP 未计入 = 预算偏低
- 冬季山区需 snow chain / 4WD
