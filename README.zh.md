# AtlasAgent

**全球高级定制化 AI 旅游攻略 Skill Pack** — 遵循 [Agent Skills 开放标准](https://agentskills.io/specification)，适用于 **任意** SKILL.md 兼容 Agent（Cursor、Claude Code、Codex、Copilot、Hermes 等）。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-green.svg)](https://agentskills.io)
[![Skills](https://img.shields.io/badge/skills-9-green.svg)](skills/)

> 零 API Key 即可起步 · 多方案对比 · 逐日行程 · 多币种预算 · 签证/饮食/交通决策 · PDF 导出

<p align="center">
  <img src="docs/assets/atlas-agent-hero.jpg" alt="AtlasAgent 全球 AI 旅游攻略 Skill Pack" width="900">
</p>

## Demo 预览

<p align="center">
  <img src="docs/assets/demo-itinerary-preview.png" alt="东京 7 日行程 PDF 预览" width="720">
</p>

| 资源 | 链接 |
|------|------|
| Markdown 行程 | [examples/tokyo-7days-zh.md](examples/tokyo-7days-zh.md) |
| PDF 导出 | `python3 "$ATLAS_ROOT/scripts/md2pdf.py" examples/tokyo-7days-zh.md` |

---

## 5 分钟安装

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh all    # 或 cursor / claude / codex / hermes
pip3 install fpdf2                          # 可选，PDF 导出
python3 "$ATLAS_ROOT/scripts/weather_client.py" forecast --city Tokyo --days 3
```

> **注意：** 必须 clone **完整仓库**。只复制 `skills/` 会导致脚本和知识库失效。

详细安装：[docs/install.md](docs/install.md) · Agent 速览：[AGENTS.md](AGENTS.md)

---

## 支持的 Agent

| Agent | Skills 目录 | 安装 |
|-------|-------------|------|
| Cursor | `~/.cursor/skills/` | `bash scripts/install.sh cursor` |
| Claude Code | `~/.claude/skills/` | `bash scripts/install.sh claude` |
| Codex | `~/.codex/skills/` | `bash scripts/install.sh codex` |
| Copilot / OpenCode | `~/.agents/skills/` | `bash scripts/install.sh copilot` |
| Hermes（可选） | `~/.hermes/skills/productivity/` | `bash scripts/install.sh hermes` |

---

## Skill 清单

| Skill | 说明 |
|-------|------|
| **[atlas-agent](skills/atlas-agent/SKILL.md)** | 主编排器 |
| [weather](skills/weather/SKILL.md) | Open-Meteo 天气预报 |
| [currency](skills/currency/SKILL.md) | 多币种换算 |
| [visa-entry](skills/visa-entry/SKILL.md) | 签证/入境 |
| [dietary-global](skills/dietary-global/SKILL.md) | 饮食限制 |
| [transport-global](skills/transport-global/SKILL.md) | 交通决策 |
| [local-intel](skills/local-intel/SKILL.md) | 口碑调研 |
| [travel-documents](skills/travel-documents/SKILL.md) | 证件清单 |
| [budget-optimizer](skills/budget-optimizer/SKILL.md) | 预算优化 |

---

## 能力层级

| 层级 | 能力 | API Key |
|------|------|---------|
| **L0** | 脚本 + 目的地知识库 | 否 |
| **L1** | trvl MCP、Reddit/YouTube 调研 | 可选 |
| **L2** | Amadeus、日历/文档导出 | 需配置 |

---

## 项目结构

```
AtlasAgent/
├── skills/              # 9 个 Agent Skills（agentskills.io 格式）
├── scripts/             # 共享 CLI + install.sh
├── skills/atlas-agent/references/destinations/  # 目的地知识库（欢迎 PR）
├── examples/
└── docs/install.md
```

---

## 贡献

PR 添加 `skills/atlas-agent/references/destinations/<city>.md` — 模板见 [_template.md](skills/atlas-agent/references/destinations/_template.md)

---

## License

MIT — 详见 [LICENSE](LICENSE)

English README: [README.md](README.md)
