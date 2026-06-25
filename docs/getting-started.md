# 入门指南

详见 **[安装指南 install.md](install.md)**（支持 Cursor / Claude Code / Codex / Copilot / Hermes 等）。

## 最短路径

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh cursor   # 或 all / claude / codex
pip3 install fpdf2                            # 可选
```

## 验证

```bash
python3 "$ATLAS_ROOT/scripts/weather_client.py" forecast --city Tokyo --days 3
```

## 示例 Prompt

```
帮我规划 2026年10月1日-7日 东京 7 天 2 人行程。
出发地：上海。预算人均 8000 人民币。
偏好：美食 + 拍照。不吃辣。输出中文。
```

## 导出 PDF

```bash
python3 "$ATLAS_ROOT/scripts/md2pdf.py" examples/tokyo-7days-zh.md
```

## Agent 无关说明

- Skills 内容不绑定 Hermes / Cursor 专有 API
- 编排逻辑在 `skills/atlas-agent/SKILL.md`
- 运行时脚本在 `$ATLAS_ROOT/scripts/`
- 目的地知识库在 `skills/atlas-agent/references/destinations/`

## 更多

- [AGENTS.md](../AGENTS.md) — 一页速览
- [architecture.md](architecture.md) — 架构
- [mcp/recommended-servers.md](../mcp/recommended-servers.md) — MCP 增强
