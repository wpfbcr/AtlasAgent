# AtlasAgent

**全球高级定制化 AI 旅游攻略 Skill Pack** — 为 Hermes / Cursor / Claude Code 等 Agent 提供即插即用的行程规划能力。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-9-green.svg)](skills/)

> 零 API Key 即可起步 · 多方案对比 · 逐日行程 · 多币种预算 · 签证/饮食/交通决策 · PDF 导出

<p align="center">
  <img src="docs/assets/atlas-agent-hero.jpg" alt="AtlasAgent 全球 AI 旅游攻略 Skill Pack" width="900">
</p>

## Demo 预览

**Agent 输出示例**（东京 7 日深度游）→ 一键导出 PDF：

<p align="center">
  <img src="docs/assets/demo-itinerary-preview.png" alt="东京 7 日行程 PDF 预览" width="720">
</p>

| 资源 | 链接 |
|------|------|
| Markdown 行程 | [examples/tokyo-7days-zh.md](examples/tokyo-7days-zh.md) |
| PDF 导出 | 本地运行 `python3 scripts/md2pdf.py examples/tokyo-7days-zh.md` |
| 巴黎示例 | [examples/paris-romantic-5days-zh.md](examples/paris-romantic-5days-zh.md) |

---

## 5 分钟快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/wpfbcr/AtlasAgent.git
cd AtlasAgent

# 2. 安装到 Hermes（或复制 skills/ 到 ~/.cursor/skills/）
cp -r skills/* ~/.hermes/skills/productivity/

# 3. 安装 PDF 依赖（可选）
pip3 install fpdf2

# 4. 验证天气与汇率脚本
python3 scripts/weather_client.py forecast --city "Tokyo" --days 7
python3 scripts/currency_client.py convert 1000 --from USD --to JPY

# 5. 在 Agent 对话中启用 atlas-agent skill，输入：
# 「帮我规划 2026年7月 东京 7 天 2 人，预算人均 8000 人民币，喜欢美食和拍照」
```

完整文档见 [docs/getting-started.md](docs/getting-started.md)。

---

## 能力概览

| 层级 | 能力 | 是否需要 Key |
|------|------|-------------|
| **L0 零配置** | 地理 POI、天气预报、汇率换算、目的地知识库 | 否 |
| **L1 增强** | trvl MCP 航班/酒店、Reddit/YouTube 口碑调研 | 可选 |
| **L2 专业** | Amadeus、Google Workspace、Notion 导出 | 需 OAuth/API |

---

## Skill 清单

| Skill | 说明 |
|-------|------|
| **[atlas-agent](skills/atlas-agent/SKILL.md)** | 主编排器：全流程行程规划 |
| [weather](skills/weather/SKILL.md) | Open-Meteo 天气预报 |
| [currency](skills/currency/SKILL.md) | 多币种预算换算 |
| [visa-entry](skills/visa-entry/SKILL.md) | 签证/入境/护照有效期 |
| [dietary-global](skills/dietary-global/SKILL.md) | 全球饮食限制定制 |
| [transport-global](skills/transport-global/SKILL.md) | 租车/铁路通票/廉航决策 |
| [local-intel](skills/local-intel/SKILL.md) | Reddit/YouTube 目的地口碑 |
| [travel-documents](skills/travel-documents/SKILL.md) | 护照/保险/紧急联系清单 |
| [budget-optimizer](skills/budget-optimizer/SKILL.md) | 多方案成本优化 |

**外部依赖**（推荐安装）：
- [Hermes maps skill](https://github.com/NousResearch/hermes-agent) — 全球 geocode / POI / 路线
- [trvl MCP](https://github.com/mikkoparkkola/trvl) — 零 Key 航班/酒店搜索

---

---

## 项目结构

```
AtlasAgent/
├── skills/           # 9 个 Agent Skills
├── scripts/          # 可独立运行的 CLI 工具
├── references/       # 目的地知识库（欢迎 PR）
├── examples/         # 完整行程示例
├── mcp/              # MCP 服务器配置指南
└── docs/             # 架构与入门文档
```

---

## 贡献目的地

欢迎 PR 添加 `references/destinations/<city>.md`！模板见 [_template.md](references/destinations/_template.md)。

---

## 相关项目

- [trvl](https://github.com/mikkoparkkola/trvl) — 零 Key 旅行 MCP
- [travel-skill](https://github.com/JMMonte/travel-skill) — 航班+酒店+Airbnb MCP
- [Agent-Reach](https://github.com/Panniantong/Agent-Reach) — 全网调研路由

---

## License

MIT — 详见 [LICENSE](LICENSE)

English README: [README.md](README.md)
