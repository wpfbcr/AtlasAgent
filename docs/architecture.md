# AtlasAgent 架构

## 设计原则

1. **Agent-agnostic** — 遵循 [agentskills.io](https://agentskills.io/specification)；SKILL 正文不含 Hermes/Cursor 专有 API
2. **Full repo runtime** — `skills/` 是指令；`scripts/` 是工具；二者通过 `ATLAS_ROOT` 关联
3. **Progressive disclosure** — 主编排 `atlas-agent` + 8 个子 skill；细节在各自 `references/`
4. **Tiered capabilities** — L0 零 Key → L1 MCP/UGC → L2 专业 API

## 结构

```
AtlasAgent/
├── AGENTS.md                 # Agent 速览（任意模型可读）
├── skills/
│   ├── atlas-agent/          # 主编排 + references/destinations/
│   ├── weather/
│   └── ...                   # 8 个子 skill
├── scripts/                  # Python CLI（weather, currency, pdf, install）
├── examples/                 # 示例行程
├── mcp/                      # 可选 MCP 配置
└── docs/install.md           # 多 Agent 安装表
```

## 模块关系

```
atlas-agent
├── weather, currency     → $ATLAS_SCRIPTS/*.py
├── visa-entry, dietary-global, transport-global, … → skill references
└── destinations          → skills/atlas-agent/references/destinations/
```

## 安装模型

| 层 | 内容 | 安装方式 |
|----|------|----------|
| Skills | `skills/*/SKILL.md` | `install.sh` → ~/.cursor/skills 等 |
| Runtime | `scripts/` | 保留完整 git clone，`ATLAS_ROOT` |
| 可选 | trvl MCP, MAPS_SCRIPT | 环境变量 / MCP 配置 |

## 与 Hermes 的关系

Hermes 是 **可选** 安装目标（`install.sh hermes`）。不再在 SKILL 中硬编码 `~/.hermes` 路径或 `clarify()` 等专有工具。

## 版本

Skill pack `metadata.atlas.version`: **1.1.0** — agent-agnostic refactor
