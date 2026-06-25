# 入门指南

## 1. 安装

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git
cd AtlasAgent
```

### Hermes Agent

```bash
cp -r skills/* ~/.hermes/skills/productivity/
```

### Cursor / Claude Code

```bash
cp -r skills/* ~/.cursor/skills/
# 或项目内 .cursor/skills/
```

### 可选依赖

```bash
pip3 install fpdf2   # PDF 导出
```

### 强烈推荐：maps skill

AtlasAgent 地理能力依赖 Hermes `maps` skill：

```bash
# 若使用 Hermes Agent，maps 通常已内置
python3 ~/.hermes/skills/productivity/maps/scripts/maps_client.py search "Tokyo"
```

## 2. 验证安装

```bash
cd AtlasAgent
python3 scripts/weather_client.py forecast --city "Tokyo" --days 3
python3 scripts/currency_client.py convert 1000 --from CNY --to JPY
python3 scripts/holiday_check.py --city "Tokyo" --from 2026-10-01 --days 7
```

## 3. 使用方式

在 Agent 对话中引用 `atlas-agent` skill，示例 prompt：

```
帮我规划 2026年10月1日-7日 东京 7 天 2 人行程。
出发地：上海。预算人均 8000 人民币。
偏好：美食 + 拍照。不吃辣。输出中文。
```

Agent 将按 SKILL.md 工作流自动调用子 skills。

## 4. L1 增强：trvl MCP

见 [mcp/recommended-servers.md](../mcp/recommended-servers.md)。

## 5. 导出 PDF

```bash
# 先生成 .md 行程，再转换
python3 scripts/md2pdf.py examples/tokyo-7days-zh.md
```

## 6. 环境变量（可选）

| 变量 | 用途 |
|------|------|
| `ATLAS_ROOT` | 仓库路径，默认 `~/AtlasAgent` |

在 SKILL.md 中将 `~/AtlasAgent` 替换为实际路径。
