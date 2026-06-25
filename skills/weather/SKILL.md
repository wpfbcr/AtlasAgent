---
name: weather
description: "全球天气预报：Open-Meteo 7-16 日预报，零 API Key，支持城市名或坐标。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [weather, forecast, open-meteo, travel]
    category: productivity
    requires_toolsets: [terminal]
    related_skills: [atlas-agent]
---

# Weather Skill

使用 [Open-Meteo](https://open-meteo.com/) 免费 API 获取全球天气预报，替代 wttr.in（国内常超时）。

## When to Use

- 规划行程需要目的地未来 7–16 日天气
- 决定穿着、户外/室内活动安排
- 评估雨季/极端天气风险

## Script

```bash
WEATHER=~/AtlasAgent/scripts/weather_client.py
```

### forecast — 逐日预报

```bash
python3 $WEATHER forecast --city "Tokyo" --days 7
python3 $WEATHER forecast --lat 48.8566 --lon 2.3522 --days 5
python3 $WEATHER forecast --city "Sydney" --days 10 --json
```

输出：日期、天气描述、最高/最低温、降水量、降水概率、最大风速。

### current — 当日概况

```bash
python3 $WEATHER current --city "Paris"
```

## Integration with atlas-agent

在 Phase 1 并行调用，结果写入行程「🌤️ 天气概况」模块：
- 标注数据来源与查询时间
- 雨天 → 调整户外景点到室内备选
- 高温/严寒 → 写入注意事项

## Pitfalls

- 预报精度随天数递减，7 日以上仅作趋势参考
- 南半球季节与北半球相反（6 月悉尼 = 冬季）
- 山区/海岛微气候 Open-Meteo 可能偏差，标注「仅供参考」

## Verification

```bash
python3 $WEATHER forecast --city "Paris" --days 3
# 应返回 3 行逐日数据
```
