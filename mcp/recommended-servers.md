# MCP 服务器推荐配置

AtlasAgent L1 增强层可选 MCP 集成。

## trvl（推荐 — 零 API Key）

[trvl](https://github.com/mikkoparkkola/trvl) 提供航班、酒店、火车、租车搜索。

### Cursor `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "trvl": {
      "command": "trvl",
      "args": ["mcp"]
    }
  }
}
```

安装：`go install github.com/mikkoparkkola/trvl@latest` 或下载 release binary。

### 用途

- Phase 1 实时航班/酒店价格
- transport-global 成本对比

## travel-skill（航班 + 酒店 + Airbnb + 公交）

[JMMonte/travel-skill](https://github.com/JMMonte/travel-skill)

```json
{
  "mcpServers": {
    "travel": {
      "command": "uv",
      "args": ["run", "travel-mcp"]
    }
  }
}
```

需要 Playwright（酒店模块）。

## travel-mcp-server（Amadeus — 需 API Key）

[lev-corrupted/travel-mcp-server](https://github.com/lev-corrupted/travel-mcp-server)

```json
{
  "mcpServers": {
    "travel-amadeus": {
      "command": "uvx",
      "args": ["travel-mcp-server"],
      "env": {
        "AMADEUS_CLIENT_ID": "your_id",
        "AMADEUS_CLIENT_SECRET": "your_secret"
      }
    }
  }
}
```

免费层：Amadeus Self-Service API。

## 优先级建议

| 需求 | 推荐 |
|------|------|
| 零配置试用 | 不用 MCP，L0 即可 |
| 真实航班价格 | trvl |
| Airbnb + 公交 | travel-skill |
| 企业级预订 | Amadeus / mcp-travelcode |

## AtlasAgent 标注规则

使用 MCP 数据时，输出必须包含：
- 数据来源（trvl / Amadeus / ...）
- 查询时间（UTC 或本地）
- 「价格可能变动，预订前请确认」
