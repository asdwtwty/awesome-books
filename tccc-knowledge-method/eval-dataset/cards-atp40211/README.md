# ATP 4-02.11 知识卡片增补

> 本目录是论文 §5.2 七类卡片体系在 ATP 4-02.11 陆军条令场景的扩展。
> 来源: `ATP 4-02.11 Casualty Response, TCCC, and First Aid (March 2026)`
> 字段规范: 与 TCCC 卡片一致

## 1. 增补依据

ATP 4-02.11 是陆军伤员响应、战术战斗伤员护理和急救的**主要条令文献**(254 页),除引用 TCCC 外还有大量 TCCC 不覆盖的内容:

1. **伤员收容点 (CCP) 选址与建立** (Chapter 1)
2. **三梯次施救职责详细分工** (Table 1-1)
3. **陆军特有的撤运四级分类** (urgent/priority/routine/RTD)
4. **战场速估手法**(止血带 1 分钟应用窗、烧伤手掌法)
5. **非战术急救程序**(海姆立克气道梗阻处置)

TCCC 卡片清单 (214 张候选) 不覆盖以上任何一项。本目录补充 9 张卡片。

## 2. 卡片清单

| Card ID | 标题 | ATP 章节 | 增补理由 |
|---|---|---|---|
| `ATP-TIER-001` | 三梯次职责: All Service / CLS / Combat Medic | Ch.1 Table 1-1 | TCCC PHASE 6 张未覆盖梯次分工 |
| `ATP-CCP-001` | 伤员收容点选址与建立 6 项 | Ch.1 §1-28 | TCCC EVAC 不含 CCP 建立 |
| `ATP-EVAC-001` | 撤运四级: Urgent/Priority/Routine/RTD | Ch.1 §1-55 | TCCC TRIAGE 用 MASCAL 颜色,陆军用 4 级 |
| `ATP-TQ-001` | 止血带 1 分钟应用窗与 3 分钟致死时间 | Ch.3 §3-75 | TCCC 仅说 immediate,ATP 给定时窗 |
| `ATP-CHOKE-001` | 气道梗阻识别与海姆立克 (含特殊体型替代) | Ch.5 §5-31 | TCCC AIR 12 张未给出非创伤气道处置 |
| `ATP-CHESTSEAL-001` | 多胸部伤口处置原则 (一发现一处理) | Ch.6 §6-26 | TCCC RESP-013 不覆盖多伤口决策 |
| `ATP-PRESSDRES-001` | 加压敷料 4 项复评要点 | Ch.7 §7-22 | TCCC HEM-018 仅止血带复评 |
| `ATP-EYE-001` | 眼外伤分型识别 (眼睑/眼球/强光) | Ch.10 §10-1~2 | TCCC EYE 4 张未明确分型 |
| `ATP-BURN-001` | 烧伤手掌法 ≈1% + Rule of Nines 速估 | Ch.12 §12-5 | TCCC BURN-004 未给战场速估手法 |

## 3. 字段约定

`module=ATP` 已在 `kbtool/validate.py` 词表注册。
`source_id` 统一为 `ATP-4-02.11`,引用页码精确到节号(便于 §10.5.6 的字段级追溯)。

## 4. 与 TCCC 关系

ATP 4-02.11 章节大量引用 TCCC,因此本目录卡片倾向于:
- 若 TCCC 已覆盖,则不重复
- 若 ATP 提供更具体的时间窗、空间结构、SOP,则增补一张
