# 贡献指南

感谢考虑为 AtlasAgent 贡献！

## 最欢迎的贡献：目的地知识库

1. 复制 `references/destinations/_template.md`
2. 命名为 `references/destinations/<city-name>.md`（英文小写+连字符）
3. 填写真实、可验证的数据
4. 在文件末尾标注 `最后更新：YYYY-MM-DD`
5. 提交 PR

### 质量标准

- 门票/交通价格用区间，标注币种
- 不抄袭 OTA/攻略网站大段文字
- 闭馆日/预约要求必须准确或标注「请查官网」
- 签证信息仅作参考，指向官方链接

## 贡献 Skill 改进

- 修改 `skills/*/SKILL.md` 请保持 Hermes frontmatter 格式
- 新脚本放 `scripts/`，需 stdlib 或注明 pip 依赖
- 中英文：用户面向文档中文优先

## 本地验证

```bash
python3 scripts/weather_client.py forecast --city "YourCity" --days 3
python3 scripts/holiday_check.py --from 2026-07-01 --days 5 --city "YourCity"
```

## Code of Conduct

友善、包容、就事论事。

## License

贡献内容以 MIT 协议发布。
