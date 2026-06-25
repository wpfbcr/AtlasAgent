# AtlasAgent — 安装指南

## For Humans（复制给 AI Agent）

复制这句话给你的 AI Agent（Cursor、Claude Code、Codex、OpenClaw 等）：

```
帮我安装 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/install.md
```

> 已安装过？更新也是一句话：
> ```
> 帮我更新 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/update.md
> ```

> 安全模式（不自动改 shell 配置、不自动 pip 安装）：
> ```
> 帮我安装 AtlasAgent（安全模式）：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/install.md
> 安装时使用 --safe 参数
> ```

---

## For AI Agents

### Goal

Install AtlasAgent so the user can plan **global travel itineraries** with 9 Agent Skills + Python CLI tools. After install, read `skills/atlas-agent/SKILL.md` and use `$ATLAS_ROOT/scripts/` for weather, currency, calendar, and PDF export.

AtlasAgent is **agent-agnostic** — not tied to Hermes or any single product.

### Boundaries

When installing, stay within these limits:

- **DO NOT** run `sudo` unless the user explicitly approved
- **DO NOT** modify system files outside `~/.cursor/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, `~/.hermes/skills/`, `~/AtlasAgent/`, and the user's shell rc (unless `--safe`)
- **DO NOT** install packages not listed in this guide (allowed: `fpdf2` for PDF)
- **DO NOT** clone repos or create AtlasAgent files inside the user's **project workspace** — use `~/AtlasAgent/`

### Directory Rules

| Purpose | Directory |
|---------|-----------|
| Full repo (scripts + skills + references) | `~/AtlasAgent/` or `$ATLAS_ROOT` |
| Installed skills | `~/.cursor/skills/`, `~/.claude/skills/`, etc. |
| Temp output | `/tmp/` |

**Why?** Copying only `skills/` breaks weather/currency scripts. Always clone the **full repository**.

### Step 1: Clone repository

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
```

If already cloned:

```bash
git -C ~/AtlasAgent pull
export ATLAS_ROOT=~/AtlasAgent
```

### Step 2: Install skills + runtime

```bash
bash ~/AtlasAgent/scripts/atlas-agent install --env=auto --agent=all
```

Or target one agent:

```bash
bash ~/AtlasAgent/scripts/atlas-agent install --agent=cursor
bash ~/AtlasAgent/scripts/atlas-agent install --agent=claude
bash ~/AtlasAgent/scripts/atlas-agent install --agent=codex
bash ~/AtlasAgent/scripts/atlas-agent install --agent=copilot
bash ~/AtlasAgent/scripts/atlas-agent install --agent=hermes
```

**Safe mode / Dry run:**

```bash
bash ~/AtlasAgent/scripts/atlas-agent install --env=auto --safe
bash ~/AtlasAgent/scripts/atlas-agent install --env=auto --dry-run
```

This installs:

1. All 9 skills into the agent's skills directory
2. `ATLAS_ROOT` in `~/.zshrc` or `~/.bashrc` (unless `--safe`)
3. Optional: `pip3 install fpdf2` for PDF export

**L0 zero-config channels (no API key):**

- Weather → Open-Meteo (`weather_client.py`)
- Currency → Frankfurter/ECB (`currency_client.py`)
- Calendar hints → `holiday_check.py`
- Destination knowledge → `skills/atlas-agent/references/destinations/`

### Step 3: Ask user about optional enhancements

After L0 works, **ask the user** which extras they want:

> 基础能力已就绪！你现在可以让我规划全球行程、预算、签证提醒等。
>
> 可选增强，你需要哪些？
>
> - 🗺️ **地理 POI** — 设置 `MAPS_SCRIPT` 指向 geocode/POI CLI（或我用 web 搜索 + 知识库）
> - ✈️ **实时航班/酒店** — 配置 trvl MCP（零 API Key）
> - 💬 **口碑调研** — Reddit/YouTube（Agent-Reach 或 web 搜索）
> - 📄 **PDF 导出** — `pip3 install fpdf2`（若未安装）
>
> 告诉我你要哪些，或说「先用基础版」。

Based on choice, see [mcp/recommended-servers.md](../mcp/recommended-servers.md).

### Step 4: Run doctor

```bash
bash ~/AtlasAgent/scripts/atlas-agent doctor
# or JSON: bash ~/AtlasAgent/scripts/atlas-agent doctor --json
```

Fix any ❌/⚠️ before telling the user installation is complete.

### Step 5: Register usage

Ensure the agent can load `atlas-agent` skill (or read `~/AtlasAgent/skills/atlas-agent/SKILL.md`). User can say:

> 帮我规划 2026年10月 东京 7 天 2 人，预算人均 8000 人民币，不吃辣。

---

## Quick Reference

| Command | What it does |
|---------|--------------|
| `atlas-agent install --env=auto` | Clone path + install all skills |
| `atlas-agent install --agent=cursor` | Install to Cursor only |
| `atlas-agent install --safe` | Print manual steps only |
| `atlas-agent install --dry-run` | Preview actions |
| `atlas-agent doctor` | Health check |
| `atlas-agent check-update` | How to pull latest |

| Script | Example |
|--------|---------|
| Weather | `python3 "$ATLAS_ROOT/scripts/weather_client.py" forecast --city Tokyo --days 7` |
| Currency | `python3 "$ATLAS_ROOT/scripts/currency_client.py" convert 8000 --from CNY --to JPY` |
| Calendar | `python3 "$ATLAS_ROOT/scripts/holiday_check.py" --from 2026-10-01 --days 7 --city Tokyo` |
| PDF | `python3 "$ATLAS_ROOT/scripts/md2pdf.py" examples/tokyo-7days-zh.md` |

## Manual install (no Agent)

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh cursor
pip3 install fpdf2
bash ~/AtlasAgent/scripts/atlas-agent doctor
```

## Skill locations by agent

| Agent | Skills directory |
|-------|------------------|
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Copilot / OpenCode | `~/.agents/skills/` |
| Hermes (optional) | `~/.hermes/skills/productivity/` |

## Uninstall

```bash
rm -rf ~/.cursor/skills/atlas-agent ~/.cursor/skills/weather ~/.cursor/skills/currency \
       ~/.cursor/skills/visa-entry ~/.cursor/skills/dietary-global \
       ~/.cursor/skills/transport-global ~/.cursor/skills/local-intel \
       ~/.cursor/skills/travel-documents ~/.cursor/skills/budget-optimizer
# Repeat for ~/.claude/skills/ etc.
# Remove ATLAS_ROOT line from ~/.zshrc if desired
# rm -rf ~/AtlasAgent
```
