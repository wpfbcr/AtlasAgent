# 从 travel-planning 迁移

旧版 Hermes `travel-planning`（中国境内专用）已由 **AtlasAgent** 替代。

## 新安装方式（Agent 无关）

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh hermes   # 若使用 Hermes
# 或 install.sh cursor / claude / codex / all
rm -rf ~/.hermes/skills/productivity/travel-planning   # 可选，移除旧 skill
```

## 主要变化

| 旧版 | AtlasAgent |
|------|------------|
| 仅 Hermes 路径 | `ATLAS_ROOT` + 多 Agent install.sh |
| `clarify()` 等 Hermes API | 通用「向用户追问」 |
| `~/.hermes/.../maps` 硬依赖 | 可选 `MAPS_SCRIPT` 或 web + 知识库 |
| 中国境内 | 全球 |

## 知识库路径

原 `xian-destinations.md` 等内容可 PR 到：

`skills/atlas-agent/references/destinations/`
