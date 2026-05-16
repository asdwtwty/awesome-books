# PCC (Prolonged Casualty Care) 知识卡片增补

> 本目录是论文 §5.2 七类卡片体系在 PCC 长时程救护场景的扩展。
> 来源: `Prolonged Casualty Care Guidelines (JTS CPG ID:91)`
> 字段规范: 与 TCCC 卡片一致 (见 `../tccc-zip-unpacked/TCCC指南知识卡片/3.知识卡片字段构建规范/`)

## 1. 增补依据

TCCC 卡片清单 (214 张候选) 仅覆盖 `prolonged_care_reference` 阶段(被动引用),**未对 PCC 独立场景给出卡片**。这与论文 §1.2 特点(7)伤员队列动态变化、(8)证据要求强可追溯的需求不符。

本目录对照 PCC CPG 全文(75 页),提取 16 个章节中 TCCC 未覆盖的关键决策点,补充 11 张卡片。

## 2. 卡片清单

| Card ID | 标题 | PCC CPG 章节 | 增补理由 |
|---|---|---|---|
| `PCC-PRIN-001` | PCC 阶段总体目标与团队职责分配 | PCC PRINCIPLES p.6-7 | 总纲: 'get out of PCC' + team leader |
| `PCC-PRIN-002` | PCC 全身体格检查与生命体征趋势记录 | PCC PRINCIPLES p.7 | TCCC 不要求趋势化记录 |
| `PCC-MASCAL-001` | PCC 环境下 MASCAL 资源管理与连续分诊 | MASCAL/TRIAGE p.9-10 | TCCC TRIAGE 6 张仅覆盖一次性分诊 |
| `PCC-HEM-001` | PCC 大出血控制的角色分级要求 (ASM→CPP) | MASSIVE HEMORRHAGE p.11-12 | TCCC HEM 24 张未提及 PCC 角色分级 |
| `PCC-CIRC-001` | PCC 循环复苏目标与休克分型 | CIRCULATION p.17-19 | TCCC CIRC-013 SBP 80-90; PCC 是 100-110 |
| `PCC-COMM-001` | PCC 远程会诊与文书 (DD Form 1380 + Flowsheet) | COMMUNICATION p.20-21 | TCCC EVAC-004 不覆盖 teleconsultation |
| `PCC-HYP-001` | PCC 长时程低体温预防 (>10h 加温毯更换) | HYPOTHERMIA p.22-23 | TCCC HYP 9 张不覆盖 >10h 长程 |
| `PCC-HEAT-001` | PCC 热射病与热衰竭鉴别 | HYPERTHERMIA p.24-25 | TCCC 不覆盖热射病 |
| `PCC-SEPSIS-001` | PCC 脓毒症识别与三档抗感染方案 | ANTIBIOTICS p.40 Table 14 | TCCC ABX 5 张不覆盖脓毒症升级 |
| `PCC-NURS-001` | PCC 护理与伤口换药频率体系 | NURSING p.43-45 Table 17 | TCCC WOUND 8 张不覆盖长程护理 |
| `PCC-SPLINT-001` | PCC 长时程夹板与担架填充分级 | SPLINTING p.46 Table 18 | TCCC MSK 3 张不覆盖长时程 |

## 3. 字段约定

新增 `module=PCC` 与 `applicable_phase=prolonged_casualty_care`,均已在 `kbtool/validate.py` 词表中注册。

## 4. 跨模块引用(Pending)

PCC 卡片中的 `related_cards` 引用 TCCC 模块 (CIRC, EVAC, HYP, ABX, MSK 等),目前 zip 中只实现 HEM 24 张。validate 会发出 ref_target warning,这是预期行为——待补全 TCCC 其余模块后会自动消除。
