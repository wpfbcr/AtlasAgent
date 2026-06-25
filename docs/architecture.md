# AtlasAgent 架构说明

## 设计原则

1. **Skill-first**：编排逻辑在 SKILL.md，可运行于 Hermes / Cursor / Claude Code
2. **零配置优先**：L0 不依赖 API Key（Open-Meteo + Frankfurter + OSM）
3. **渐进增强**：L1 MCP / L2 OAuth 按需启用
4. **不虚构数据**：API 失败时标注「估算，出行前验证」

## 模块关系

```
atlas-agent (主编排)
├── weather          → scripts/weather_client.py
├── currency         → scripts/currency_client.py
├── visa-entry       → references/visa-quick-ref.md + web
├── dietary-global   → references/dietary-playbooks.md
├── transport-global → references/transport-guides.md
├── local-intel      → agent-reach / web_search
├── travel-documents → references/document-addons.md
├── budget-optimizer → currency + 模板
└── maps (外部)      → Hermes maps skill
```

## 三层能力

| 层级 | 组件 |
|------|------|
| L0 | maps + Open-Meteo + Frankfurter + references/destinations |
| L1 | trvl MCP + Agent-Reach |
| L2 | Amadeus + Google Workspace + Notion |

## 数据流

```
用户输入 → Phase 0 约束收集
         → Phase 1 并行数据采集
         → Phase 1.5 消歧
         → Phase 2 排程工程
         → Phase 3 行程 + 预算
         → Phase 4 方案对比
         → Phase 5 导出 (MD/PDF/Obsidian/Notion)
```

## 与旧 travel-planning 的关系

AtlasAgent **完全替代** Hermes `travel-planning`（中国境内专用）。全球场景统一由 `atlas-agent` 处理，中国境内游作为全球子集（references 可扩展中国城市）。
