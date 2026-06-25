# AtlasAgent

**Global AI travel planning skill pack** for Hermes, Cursor, Claude Code, and any MCP-compatible agent.

> Zero API keys to start · Multi-plan comparison · Day-by-day itineraries · Multi-currency budgets · Visa/diet/transport decisions · PDF export

**中文文档（主文档）**: [README.zh.md](README.zh.md)

<p align="center">
  <img src="docs/assets/atlas-agent-hero.jpg" alt="AtlasAgent travel planning skill pack" width="900">
</p>

## Demo

Sample output: [Tokyo 7-day itinerary](examples/tokyo-7days-zh.md) → PDF export

<p align="center">
  <img src="docs/assets/demo-itinerary-preview.png" alt="Tokyo itinerary PDF preview" width="720">
</p>

## Quick Start

```bash
git clone https://github.com/wpfbcr/AtlasAgent.git
cd AtlasAgent
cp -r skills/* ~/.hermes/skills/productivity/
pip3 install fpdf2
python3 scripts/weather_client.py forecast --city Tokyo --days 7
```

See [docs/getting-started.md](docs/getting-started.md) for full setup.

## Skills

| Skill | Purpose |
|-------|---------|
| `atlas-agent` | Main orchestrator |
| `weather` | Open-Meteo forecasts |
| `currency` | Multi-currency conversion |
| `visa-entry` | Visa & entry requirements |
| `dietary-global` | Dietary restrictions worldwide |
| `transport-global` | Car rental / rail pass / budget airline decisions |
| `local-intel` | Reddit/YouTube destination research |
| `travel-documents` | Passport/insurance checklists |
| `budget-optimizer` | Cost optimization across plans |

## License

MIT — see [LICENSE](LICENSE)
