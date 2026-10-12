# 贡献指南

## 目的地知识库

1. 复制 [skills/atlas-agent/references/destinations/_template.md](skills/atlas-agent/references/destinations/_template.md)
2. 保存为 `skills/atlas-agent/references/destinations/<city-name>.md`
3. 标注 `最后更新：YYYY-MM-DD`
4. 提交 PR

## Skill 规范

遵循 [agentskills.io](https://agentskills.io/specification)：

- Frontmatter 必需：`name`（= 目录名）、`description`（第三人称 + 触发词）
- 可选：`license`、`compatibility`、`metadata.atlas`
- **不要**在 SKILL 正文中绑定单一 Agent 的专有 API
- 脚本路径使用 `$ATLAS_ROOT/scripts/`，不要硬编码 `~/.hermes` 等

## 验证

离线回归检查（安装测试仅写入临时目录，不修改真实的用户配置）：

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
for script in scripts/install.sh scripts/atlas-agent scripts/atlas-env.sh; do
  bash -n "$script" || exit 1
done
```

可选的联网连通检查：

```bash
export ATLAS_ROOT="$(pwd)"
python3 scripts/weather_client.py forecast --city Paris --days 3
```

## License

MIT — 贡献以 MIT 发布
