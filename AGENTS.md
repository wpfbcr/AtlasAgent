# AtlasAgent — Agent Quick Reference

Global travel planning skill pack. **Agent-agnostic** (not Hermes-specific).

## One-line install (give this URL to any Agent)

```
帮我安装 AtlasAgent：https://raw.githubusercontent.com/wpfbcr/AtlasAgent/main/docs/install.md
```

Full guide: [docs/install.md](docs/install.md)

## After install

```bash
export ATLAS_ROOT="${ATLAS_ROOT:-$HOME/AtlasAgent}"
bash "$ATLAS_ROOT/scripts/atlas-agent doctor"
```

## Skills (9)

Start with `atlas-agent` → delegate to weather, currency, visa-entry, dietary-global, transport-global, local-intel, travel-documents, budget-optimizer as needed.

## Paths

```bash
ATLAS_SCRIPTS="$ATLAS_ROOT/scripts"
ATLAS_REF="$ATLAS_ROOT/skills/atlas-agent/references"
```

## Optional

- `MAPS_SCRIPT` — geocode/POI CLI
- trvl MCP — flights/hotels ([mcp/recommended-servers.md](mcp/recommended-servers.md))
- Agent-Reach — Reddit/YouTube research

## License

MIT
