---
name: travel-documents
description: "旅行证件清单：护照/签证/保险/疫苗/紧急联系/大使馆，出发前 checklist。"
version: 1.0.0
author: AtlasAgent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [passport, insurance, emergency, checklist, travel]
    category: productivity
    requires_toolsets: [terminal, web]
    related_skills: [atlas-agent, visa-entry]
---

# Travel Documents Skill

生成出发前证件与应急准备清单，嵌入 atlas-agent 每个方案的「📋 证件/保险清单」模块。

## When to Use

- 任何跨国行程的方案输出
- 用户首次出境或去陌生地区
- 冒险/偏远目的地（沙漠/登山/潜水）

## Checklist Template

### 证件 Essentials

- [ ] 护照（有效期 ≥6 个月，≥2 空白页）
- [ ] 签证 / ESTA / eTA / EVW（见 visa-entry 输出）
- [ ] 国际驾照 IDP（如需租车，见 transport-global）
- [ ] 机票/酒店确认单（打印 + 电子版）
- [ ] 信用卡/现金（目的地货币 + 少量 USD/EUR 应急）

### 保险 Insurance

- [ ] 旅行医疗险（覆盖医疗遣返 repatriation）
- [ ] 冒险活动附加险（滑雪/潜水/登山如适用）
- [ ] 行李丢失/航班延误险（可选）
- 保额建议：医疗 ≥ $100,000 USD；申根区 ≥ €30,000

### 健康 Health

- [ ] 常规疫苗（COVID/流感按目的地要求）
- [ ] 黄热病证书（非洲/南美部分国家）
- [ ] 个人常备药 + 处方翻译件
- [ ] 过敏卡（多语言，见 dietary-global）

### 数字 Digital

- [ ] eSIM / 国际漫游 / 便携 WiFi
- [ ] 离线地图（Google Maps / Maps.me）
- [ ] 护照/签证扫描件存云端 + 纸质备份

### 紧急 Emergency

```
🆘 紧急号码：[目的地] 112/911/119/999
🏛️ 本国大使馆：[城市] [地址] [电话] [网址]
📞 旅行保险理赔热线：[号码]
👤 国内紧急联系人：[姓名] [电话]
```

用 web_search 查 `[国籍] embassy [destination city]` 获取最新使馆信息。

## Destination-Specific Add-ons

详见 `references/document-addons.md`：
- 欧盟：EHIC/GHIC（英国公民）
- 美国：ESTA 打印确认
- 日本：Visit Japan Web（入境审查）
- 澳大利亚：入境卡 / SmartGate

## Integration

`atlas-agent` Phase 3 每个方案末尾输出完整 checklist，出发前 7 天提醒用户逐项确认。

## Pitfalls

- 使馆地址/电话变动，必须 web 核实
- 旅行保险「已有疾病」除外条款需告知用户
- 不要存储用户护照号码在日志中
