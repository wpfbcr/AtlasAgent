# AtlasAgent

**Global AI travel planning skill pack** — [Agent Skills](https://agentskills.io/specification) compatible. Works with **any** agent that loads `SKILL.md` (Cursor, Claude Code, Codex, Copilot, Hermes, …).

**中文文档**: [README.zh.md](README.zh.md)

<p align="center">
  <img src="docs/assets/atlas-agent-hero.jpg" alt="AtlasAgent travel planning skill pack" width="900">
</p>

## Install

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh all
```

Full repo required — copying `skills/` alone breaks scripts. See [docs/install.md](docs/install.md).

## Skills

9 skills: `atlas-agent` (orchestrator) + weather, currency, visa-entry, dietary-global, transport-global, local-intel, travel-documents, budget-optimizer.

See [AGENTS.md](AGENTS.md) for a one-page overview.

## License

MIT
