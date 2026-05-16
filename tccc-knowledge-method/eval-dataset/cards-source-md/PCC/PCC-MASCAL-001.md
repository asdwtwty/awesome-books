---
card_id: PCC-MASCAL-001
title: PCC 环境下 MASCAL 资源管理与连续分诊
version: '1.0'
module: PCC
topic: MASCAL/Triage
task_type: triage
training_use:
- fact_qa
- case_qa
- structured_decision
- retrieval
difficulty: advanced
applicable_phase:
- prolonged_casualty_care
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 多名战伤伤员同时存在
related_cards:
- PCC-PRIN-001
- PCC-COMM-001
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: MASCAL/TRIAGE - PCC
  locator: p.9-10 Key Considerations
  quote: MASCAL in a PCC environment will necessitate more conservative resource allocation than traditional MASCAL... Triage
    is a continuous process and should be repeated as often as is clinically and operationally practical.
---

# PCC 环境下 MASCAL 资源管理与连续分诊

## 1. 核心问题

PCC 环境下的 MASCAL 与传统 MASCAL 在资源分配上有何不同


## 2. 输出目标

让模型输出 PCC MASCAL 的资源保守原则 + 连续分诊 + 战术指挥联合介入


## 3. 适用场景与边界

**适用场景**:
- 远程哨所
- 撤运中断的偏远阵地

**前置条件**:
- 医疗资源补给受限
- 短时间内无法后送

**不覆盖范围**:
- 不覆盖固定医院 MASCAL 流程


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 比传统 MASCAL 更保守地分配资源,优先保护稀缺资源 (如全血) | immediate | 进入 MASCAL | 立即 | PCC CPG 强调 'simpler is better' |
| 2 | 把分诊视为持续过程,临床或战术条件改变时立即重做 | high | 整个 MASCAL 期间 | 持续 | Continuous re-triage |
| 3 | 由最有经验的成员建立 MASCAL 角色与职责 | immediate | MASCAL 启动 | 立即 | 明确指挥链 |
| 4 | 战术指挥必须全程参与 MASCAL 响应 | immediate | 整个 MASCAL 期间 | 持续 | PCC CPG 第 4 条 |


## 6. 决策点

**1.**
- 如果(condition):稀缺资源 (如低滴度 O 型全血) 储备紧张
- 则(next_action):保留给最可能从中获益的伤员,而非平均分配
- 依据(rationale):PCC 资源不可指望持续补给
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 按传统 MASCAL 思路分配资源
- 一次性分诊后不再复评
- 战术指挥被排除在医疗决策外


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `MASCAL/TRIAGE - PCC`
  - 位置: `p.9-10 Key Considerations`
  - 原文引用:
    > MASCAL in a PCC environment will necessitate more conservative resource allocation than traditional MASCAL... Triage is a continuous process and should be repeated as often as is clinically and operationally practical.


## 9. 评分要点(LLM 评测)

- 是否提到 PCC MASCAL 资源更保守
- 是否提到分诊是连续过程
- 是否提到战术指挥必须参与
- 是否提到由最有经验者分配 MASCAL 角色


## 10. 备注

新增依据: PCC CPG 增补 MASCAL 卡 (TCCC 卡片清单中未覆盖)

