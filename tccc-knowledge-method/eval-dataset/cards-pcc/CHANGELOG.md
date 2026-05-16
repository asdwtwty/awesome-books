# PCC + ATP 卡片增补 — 修改清单

> 本次修订日期: 2026-05-16
> 触发: 用户上传 `TCCC指南知识卡片.zip` 后,审核发现 PCC 与 ATP 4-02.11 内容缺失
> 处理人: 按论文 §5 卡片模型 + §10 评测覆盖要求增补

## 修改类型说明

- **[NEW]** 新增卡片
- **[REVIEW-OK]** 审核通过,无需改动
- **[FOLLOWUP]** 后续工作建议

---

## A. 已有 24 张 HEM 卡的审核结果

24 张 HEM 卡审核结果: **[REVIEW-OK]**

理由:
1. 全部符合 schema 规范 (见 `kbtool/validate.py` 跑出 0 error)
2. 每张卡片单问题、有完整 source_refs 引用 TCCC 2026
3. 4 条 warning 均为 cross-module 引用 (AIR-006/EYE-001/CIRC-001/CIRC-007),属预期

不做改动,仅补齐其依赖的跨模块卡片。

---

## B. 新增 PCC 卡片清单 (11 张)

| Card ID | 模块 | 任务类型 | 增补依据 |
|---|---|---|---|
| `PCC-PRIN-001` | PCC | decision | PCC CPG p.6-7 PRINCIPLES Step 1-2 |
| `PCC-PRIN-002` | PCC | procedure | PCC CPG p.7 PRINCIPLES Step 3-5 |
| `PCC-MASCAL-001` | PCC | triage | PCC CPG p.9-10 MASCAL/TRIAGE |
| `PCC-HEM-001` | PCC | decision | PCC CPG p.11-12 Table 2 |
| `PCC-CIRC-001` | PCC | decision | PCC CPG p.17-19 CIRCULATION + Table 5 |
| `PCC-COMM-001` | PCC | documentation | PCC CPG p.20-21 Table 6 |
| `PCC-HYP-001` | PCC | procedure | PCC CPG p.22-23 HYPOTHERMIA |
| `PCC-HEAT-001` | PCC | decision | PCC CPG p.24-25 HYPERTHERMIA |
| `PCC-SEPSIS-001` | PCC | decision | PCC CPG p.40 Table 14 |
| `PCC-NURS-001` | PCC | procedure | PCC CPG p.43-45 Table 17 |
| `PCC-SPLINT-001` | PCC | procedure | PCC CPG p.46 Table 18 |

---

## C. 新增 ATP 4-02.11 卡片清单 (9 张)

| Card ID | 模块 | 任务类型 | 增补依据 |
|---|---|---|---|
| `ATP-TIER-001` | ATP | decision | ATP Chapter 1 Table 1-1 (Medical Tier) |
| `ATP-CCP-001` | ATP | procedure | ATP §1-28 (CCP Site Selection) |
| `ATP-EVAC-001` | ATP | triage | ATP §1-55 (Casualty Classification) |
| `ATP-TQ-001` | ATP | recognition | ATP §3-75 (TQ Time Window) |
| `ATP-CHOKE-001` | ATP | procedure | ATP §5-31 (Heimlich Maneuver) |
| `ATP-CHESTSEAL-001` | ATP | decision | ATP §6-26 (Multiple Chest Wounds) |
| `ATP-PRESSDRES-001` | ATP | reassessment | ATP §7-22 (Pressure Bandage Reassess) |
| `ATP-EYE-001` | ATP | recognition | ATP Ch.10 §10-1~2 (Eye Trauma Classification) |
| `ATP-BURN-001` | ATP | procedure | ATP §12-5 (Burn TBSA Palm Method) |

---

## D. 字段规范扩展

为支持 PCC/ATP 卡片,在 `kbtool/validate.py` 词表中增加:

```python
VOCAB["module"]            ∋ "PCC", "ATP"
VOCAB["applicable_phase"]  ∋ "prolonged_casualty_care"
```

## E. 卡片 ID 命名扩展

原命名规则 `^[A-Z]+-\d{3}$` 扩展为:

```python
CARD_ID_PATTERN = r"^(?:[A-Z]+-)?[A-Z]+-\d{3}$"
```

允许:
- 原有: `HEM-001`, `AIR-002`
- 新增: `PCC-CIRC-001`, `ATP-CCP-001`

## F. 校验结果

44 张卡片 (HEM 24 + PCC 11 + ATP 9) 一起跑 validate:

```
[validate] scanned: 44 cards | errors: 0 | warnings: 30
```

30 条 warning 全部为 `ref_target` (引用了 TCCC 待实现卡片 ID),属预期。0 error 表示 schema 完全合规。

## G. [FOLLOWUP] 后续建议

按 TCCC 卡片清单 §3.4-§3.16 实施剩余 190 张:

| 模块 | 数量 | 优先级 |
|---|---|---|
| AIR | 13 | High |
| RESP | 22 | High |
| CIRC | 16 | High |
| TBI | 21 | High |
| PAIN | 20 | High |
| BURN | 13 | Medium |
| HYP | 9 | Medium |
| EVAC | 15 | Medium |
| 其他 8 模块 | 61 | Low |

预计完成全部 214+20=234 张卡需 4 名医学专家 × 2 周。
