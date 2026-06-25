# AtlasAgent

Global travel planning skill pack for any SKILL.md-compatible agent.

## Quick install

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git ~/AtlasAgent
export ATLAS_ROOT=~/AtlasAgent
bash ~/AtlasAgent/scripts/install.sh all   # or: cursor | claude | codex | hermes
pip3 install fpdf2                         # optional, PDF export
```

**Important:** clone the full repository. Copying `skills/` alone breaks scripts and destination references.

## Skill index

| Skill | Role |
|-------|------|
| `atlas-agent` | Main orchestrator — start here |
| `weather` | Open-Meteo forecasts |
| `currency` | Multi-currency conversion |
| `visa-entry` | Visa and entry requirements |
| `dietary-global` | Dietary restrictions worldwide |
| `transport-global` | Transport mode decisions |
| `local-intel` | Destination research (Reddit/YouTube) |
| `travel-documents` | Passport/insurance checklists |
| `budget-optimizer` | Budget tables and optimization |

## Path variables

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
export ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
export ATLAS_REF="$ATLAS_ROOT/skills/atlas-agent/references"
```

## Workflow summary

1. Collect trip inputs (origin, dates, party, budget, destination).
2. Run scripts in parallel: weather, currency, holiday calendar.
3. Load destination references from `skills/atlas-agent/references/destinations/`.
4. Build day-by-day itinerary + budget + comparison table.
5. Export Markdown or PDF via `scripts/md2pdf.py`.

## Sub-skills

Read companion skills in `skills/` when relevant — each has its own `SKILL.md`.

## Optional enhancements

- **Geography:** set `MAPS_SCRIPT` to any geocoder CLI, or use web search + references.
- **Flights/hotels:** trvl MCP — see `mcp/recommended-servers.md`.
- **Social research:** Agent-Reach or web search — see `local-intel` skill.

## Docs

- [Install guide (Chinese)](docs/install.md)
- [Getting started](docs/getting-started.md)
- [Architecture](docs/architecture.md)

## License

MIT
