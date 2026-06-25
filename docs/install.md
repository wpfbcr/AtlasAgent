# 安装指南

AtlasAgent 遵循 [Agent Skills 开放格式](https://agentskills.io/specification)（`skills/<name>/SKILL.md`），**与具体 Agent 产品无关**。

## 重要

必须 **clone 完整仓库**。只复制 `skills/` 目录会导致 `scripts/` 和目的地知识库无法使用。

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
```

## 一键安装（推荐）

自动检测并安装到常见 Agent 的 skills 目录，同时写入 `ATLAS_ROOT`：

```bash
bash ~/AtlasAgent/scripts/install.sh all
```

按 Agent 安装：

| 命令 | 目标路径 |
|------|----------|
| `bash scripts/install.sh cursor` | `~/.cursor/skills/` |
| `bash scripts/install.sh claude` | `~/.claude/skills/` |
| `bash scripts/install.sh codex` | `~/.codex/skills/` |
| `bash scripts/install.sh copilot` | `~/.agents/skills/` |
| `bash scripts/install.sh hermes` | `~/.hermes/skills/productivity/` |

Hermes 只是可选安装目标之一，并非必需。

## 手动安装

| Agent | Skills 目录 |
|-------|-------------|
| Cursor（全局） | `~/.cursor/skills/` |
| Cursor（项目） | `.cursor/skills/` 或 `.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| GitHub Copilot / OpenCode | `.agents/skills/` 或 `~/.config/agents/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Hermes | `~/.hermes/skills/productivity/` |

```bash
cp -R ~/AtlasAgent/skills/atlas-agent ~/.cursor/skills/
# 建议安装全部 9 个 skill：
cp -R ~/AtlasAgent/skills/* ~/.cursor/skills/
export ATLAS_ROOT=~/AtlasAgent
```

## npx skills（若你的 Agent 支持）

```bash
npx skills add https://github.com/wpfbcr/AtlasAgent --agent '*'
export ATLAS_ROOT=~/AtlasAgent
```

安装后仍需保留完整仓库以使用 `scripts/`。

## 环境变量

| 变量 | 说明 |
|------|------|
| `ATLAS_ROOT` | 仓库根目录，默认 `~/AtlasAgent` |
| `ATLAS_SCRIPTS` | `$ATLAS_ROOT/scripts` |
| `ATLAS_REF` | `$ATLAS_ROOT/skills/atlas-agent/references` |
| `MAPS_SCRIPT` | 可选：任意 geocode/POI CLI 路径 |

写入 shell 配置：

```bash
echo 'export ATLAS_ROOT="$HOME/AtlasAgent"' >> ~/.zshrc
```

## 可选依赖

```bash
pip3 install fpdf2   # PDF 导出
```

## 验证

```bash
python3 "$ATLAS_ROOT/scripts/weather_client.py" forecast --city Tokyo --days 3
python3 "$ATLAS_ROOT/scripts/currency_client.py" convert 1000 --from CNY --to JPY
python3 "$ATLAS_ROOT/scripts/holiday_check.py" --from 2026-10-01 --days 7 --city Tokyo
```

## 使用

无需特殊命令。Agent 会根据 `SKILL.md` 的 `description` 自动匹配，或直接说：

> 帮我规划 2026年10月 东京 7 天 2 人行程，预算人均 8000 人民币，不吃辣。

也可在支持 skill 显式调用的环境中加载 `atlas-agent`。

## 可选增强

- **地理 POI**：设置 `MAPS_SCRIPT` 指向任意 maps/geocode CLI，或用 web 搜索 + 知识库
- **航班/酒店**：trvl MCP — 见 [mcp/recommended-servers.md](../mcp/recommended-servers.md)
- **口碑调研**：Agent-Reach 或 web 搜索 — 见 `local-intel` skill
