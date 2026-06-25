# 从 travel-planning 迁移到 AtlasAgent

旧版 Hermes `travel-planning` skill 已被 **AtlasAgent** 完全替代。

## 变更摘要

| 旧版 | 新版 |
|------|------|
| 中国境内专用 | 全球任意出发地/目的地 |
| wttr.in 天气 | Open-Meteo（稳定） |
| 人民币预算 | 多币种 + Frankfurter 汇率 |
| 高铁/国内租车 | 全球交通决策矩阵 |
| 不吃辣（川菜） | dietary-global（清真/素食/过敏等） |
| 无签证模块 | visa-entry + travel-documents |

## 迁移步骤

```bash
# 1. 安装 AtlasAgent
git clone https://github.com/wpfbcr/AtlasAgent.git
cp -r AtlasAgent/skills/* ~/.hermes/skills/productivity/

# 2. 移除旧 skill（可选）
rm -rf ~/.hermes/skills/productivity/travel-planning

# 3. 验证
python3 ~/AtlasAgent/scripts/weather_client.py forecast --city "Tokyo" --days 3
```

## Prompt 变更

旧：「帮我规划成都 3 天」  
新：「帮我规划成都 3 天，出发地北京，2 人，预算人均 3000 元」— 同样支持，但输出格式升级为全球标准。

## 知识库

原 `xian-destinations.md` 内容可 PR 到 `references/destinations/` 作为中国城市条目。
