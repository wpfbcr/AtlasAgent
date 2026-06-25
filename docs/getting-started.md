# 入门指南

**推荐**：复制给 Agent 的一句话安装见 [README.zh.md](../README.zh.md)。

```
帮我安装 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/install.md
```

完整 Agent 安装步骤：[install.md](install.md)

## 手动安装

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/atlas-agent install --env=auto
bash ~/AtlasAgent/scripts/atlas-agent doctor
pip3 install fpdf2   # 可选
```

## 示例 Prompt

```
帮我规划 2026年10月1日-7日 东京 7 天 2 人行程。
出发地：上海。预算人均 8000 人民币。不吃辣。输出中文。
```

## 更新

```
帮我更新 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/update.md
```

## 更多

- [AGENTS.md](../AGENTS.md)
- [architecture.md](architecture.md)
