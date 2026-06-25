# AtlasAgent — 更新指南

## For Humans

复制给你的 AI Agent：

```
帮我更新 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/update.md
```

---

## For AI Agents

### Goal

Update AtlasAgent to the latest version and refresh installed skills.

### Steps

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"

# 1. Pull latest
git -C "$ATLAS_ROOT" pull

# 2. Re-install skills (detect user's agent or use all)
bash "$ATLAS_ROOT/scripts/atlas-agent install --env=auto --agent=all

# 3. Verify
bash "$ATLAS_ROOT/scripts/atlas-agent doctor"
```

If `git pull` fails (local changes), ask the user before resetting.

### Optional

```bash
pip3 install -U fpdf2
bash "$ATLAS_ROOT/scripts/atlas-agent check-update"
```

Report doctor output to the user. Mention new destinations or skills if CHANGELOG/README changed.
