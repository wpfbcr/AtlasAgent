---
name: local-intel
description: "目的地口碑调研：Reddit/YouTube/Twitter 真实评价聚合，识别营销帖与避坑。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, reddit, youtube, reviews, travel, local]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [atlas-agent]
---

# Local Intel Skill

通过社交媒体和 UGC 平台获取**真实**目的地口碑，补充官方/营销信息。

## When to Use

- 评估小众 vs 网红景点是否值得去
- 寻找本地人推荐的餐厅/街区
- 识别「小红书/Instagram 照骗」类陷阱
- 了解季节性 crowd/closure 实时讨论

## Data Sources（L1 增强）

推荐使用 [Agent-Reach](https://github.com/Panniantong/Agent-Reach) 或等效工具：

```bash
# Reddit — 目的地 subreddit 或搜索
# site:reddit.com Tokyo 7 days itinerary 2025

# YouTube — 近期 vlog（注意发布时间）
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"

# Twitter/X
twitter search "Paris overrated OR underrated" -n 10
```

无 Agent-Reach 时降级为 `web_search` + `web_extract`（Jina Reader）。

## Search Templates

| 意图 | 搜索模板 |
|------|----------|
| 行程参考 | `reddit r/JapanTravel [目的地] [天数] days` |
| 餐厅避坑 | `reddit [城市] restaurant tourist trap` |
| 最佳季节 | `reddit best time visit [destination]` |
| 实时状况 | `reddit [city] [month] crowd closure` |
| 视频攻略 | `youtube [city] travel guide [year]` |

## Output Structure

```
📊 口碑摘要 — [目的地]
🔥 高频推荐（≥3 来源一致）：...
⚠️ 高频避坑：...
🤔 争议点（意见分裂）：...
📅 信息时效：最新帖子日期 YYYY-MM
🔗 来源：[URL 列表]
```

## Quality Rules

1. **优先近期**（12 个月内），标注帖子日期
2. **交叉验证**：单一 Reddit 帖不做定论
3. **区分受众**：背包客 vs 亲子 vs 奢华需求不同
4. **识别营销**：新账号 + 单一餐厅反复推荐 = 可疑
5. **不替代官方**：闭馆/签证仍以官网为准

## Integration

`atlas-agent` Phase 1 并行调用（L1），结果影响 Phase 3 景点排序和避坑模块。

## Pitfalls

- Reddit 英语偏见，日本/中国目的地需补充本地平台（Agent-Reach 小红书/B站）
- YouTube 赞助内容需标注
- 部分 subreddit 禁止 itinerary 帖，改用 search
