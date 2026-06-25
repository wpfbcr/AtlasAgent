# 全球交通决策指南

## 决策树

```
目的地有成熟地铁系统？
├── 是 → 不租车，地铁+步行+偶尔打车
└── 否 → 景点是否分散 >50km？
    ├── 是 → 租车 or 包车 or 跟团
    └── 否 → 公交+打车
```

## 铁路通票速查

| Pass | 覆盖 | 何时划算 |
|------|------|----------|
| Eurail Global | 33 欧洲国 | 多国联游 5+ 段长途 |
| Swiss Travel Pass | 瑞士全境 | 含登山铁路/museum |
| JR Pass | 日本 JR 网络 | 东京-大阪-京都往返新干线 |
| BritRail | 英国 | 多城火车联游 |
| Amtrak USA Pass | 美国 | 长距离慢游 |

**规则**：用点对点票价 × 段数 vs Pass 价格，Pass 通常需 3+ 长途才划算。

## 租车注意事项

| 地区 | 左/右舵 | IDP | 备注 |
|------|---------|-----|------|
| 美国/大陆欧洲 | 右 | 建议 | 25 岁以下附加费 |
| 英国/日本/澳洲 | 左 | 建议 | 日本 IDP 必须 |
| 冰岛 | 右 | 必须 | F-road 需 4WD |
| 新西兰 | 左 | 建议 | 山路多 |

## 廉航隐性成本

- 随身行李尺寸严格
- 选座费、优先登机
- 偏远机场→市区交通费
- 改期不退

## 多城市顺序优化

使用 maps skill：
```bash
python3 $MAPS distance "City A" --to "City B"
python3 $MAPS distance "City B" --to "City C"
python3 $MAPS distance "City A" --to "City C"
```
选择总路程最短的访问顺序。
