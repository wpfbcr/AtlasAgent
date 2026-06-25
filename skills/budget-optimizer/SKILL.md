---
name: budget-optimizer
description: "多方案预算优化：交通/住宿/餐饮/门票/小费/税费分项，多币种合计与人均。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [budget, cost, optimization, travel, currency]
    category: productivity
    requires_toolsets: [terminal]
    related_skills: [atlas-agent, currency, transport-global]
---

# Budget Optimizer Skill

为 atlas-agent 的每个方案生成标准化预算表，支持多币种、小费文化、隐性成本。

## When to Use

- Phase 3 行程构建时的 💰 预算模块
- Phase 4 多方案人均预算对比
- 用户问「怎么省钱 / 预算够不够」

## Budget Table Template

```
💰 预算估算 — [方案名]
📅 汇率日期：YYYY-MM-DD（Frankfurter/ECB）
👥 人数：N 人 | 天数：D 天

| 项目 | 当地币种 | 用户币种(CNY) | 备注 |
|------|----------|---------------|------|
| 国际/城际交通 | | | 含行李费 |
| 住宿 (D×N-1 晚) | | | ¥200-500/晚档位说明 |
| 餐饮 | | | 含小费 |
| 门票/活动 | | | |
| 市内交通 | | | 地铁/打车/Pass |
| 签证/保险 | | | 一次性 |
| 购物/应急 buffer 10% | | | |
| **合计** | | | |
| **人均** | | | |
```

## Calculation Rules

使用 `currency` skill 换算：

```bash
python3 ~/AtlasAgent/scripts/currency_client.py convert <金额> --from <A> --to <B>
```

### 住宿估算档位

| 档位 | 参考（欧美/日本） | 参考（东南亚） |
|------|------------------|----------------|
| 经济 | €60-100 / ¥8000-12000 | ¥150-300 |
| 舒适 | €120-200 / ¥15000-25000 | ¥400-800 |
| 奢华 | €300+ | ¥1500+ |

### 餐饮估算

| 地区 | 2人/天参考 |
|------|-----------|
| 日本 | ¥8000-15000 |
| 西欧 | €80-150 |
| 东南亚 | ¥150-400 |
| 美国 | $80-150 + 18-20% 小费 |

### 小费 Tipping（必须单独列）

| 国家 | 规则 |
|------|------|
| 美国 | 餐厅 18-20%，酒吧 $1/杯，酒店 $2-5/天 |
| 日本 | 无小费（可能失礼） |
| 法国 | 服务费已含，可留零头 |
| 英国 | 10-12.5% |
| 泰国 | 10% 或 rounding |

### 隐性成本 Checklist

- [ ] 廉航行李费
- [ ] 城市拥堵费（伦敦/新加坡）
- [ ] 度假村费 resort fee（美国）
- [ ] 景点预约费 / 快速通道
- [ ] SIM/eSIM 费用

## Optimization Tips

当用户预算紧张时，按优先级建议：

1. 调整住宿档位（通常最大弹性）
2. 淡季/平季日期（±30% 价差）
3. 交通：廉航 + 铁路 Pass 对比
4. 免费景点 + 1-2 付费 highlight
5. 自炊/便利店 vs 餐厅（日本/欧洲）

## Integration

`atlas-agent` Phase 3 每个方案必须有完整预算表；Phase 4 对比表引用「人均预算」列。

## Pitfalls

- 不虚构精确价格 — L0 用区间估算并标注「出行前验证」
- 汇率日期必须与 currency skill 输出一致
- 儿童/老人门票折扣单独注明
