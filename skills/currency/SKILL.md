---
name: currency
description: "多币种汇率换算：Frankfurter/ECB 实时汇率，零 API Key，支持 30+ 货币。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [currency, exchange, budget, travel, frankfurter]
    category: productivity
    requires_toolsets: [terminal]
    related_skills: [atlas-agent, budget-optimizer]
---

# Currency Skill

使用 [Frankfurter API](https://www.frankfurter.app/)（欧洲央行参考汇率）进行多币种换算。

## When to Use

- 用户预算用人民币，目的地消费用日元/欧元/美元
- 对比多个方案的跨国成本
- 预算表需要双币种/多币种并列

## Script

```bash
CURRENCY=~/AtlasAgent/scripts/currency_client.py
```

### rates — 查询汇率

```bash
python3 $CURRENCY rates --base USD
python3 $CURRENCY rates --base EUR --to JPY CNY GBP
```

### convert — 金额换算

```bash
python3 $CURRENCY convert 8000 --from CNY --to JPY EUR
python3 $CURRENCY convert 150 --from EUR --to USD
```

## Integration with atlas-agent

- Phase 1 获取用户偏好币种 → 目的地币种汇率
- 预算表每行标注：**原币种 + 用户币种（汇率日期）**
- 小费/税费按目的地惯例单独列项（见 budget-optimizer）

## Common Travel Currencies

| 代码 | 地区 |
|------|------|
| USD | 美国及多数国际报价 |
| EUR | 欧元区 |
| GBP | 英国 |
| JPY | 日本 |
| CNY | 中国 |
| AUD | 澳大利亚 |
| THB | 泰国 |
| KRW | 韩国 |

## Pitfalls

- Frankfurter 不含所有小币种，缺失时用 web_search 补充并标注来源
- 机场/酒店兑换汇率显著差于 ECB 参考价，提醒用户用 ATM/信用卡
- 预算表必须标注 `汇率日期: YYYY-MM-DD`

## Verification

```bash
python3 $CURRENCY convert 100 --from USD --to JPY
```
