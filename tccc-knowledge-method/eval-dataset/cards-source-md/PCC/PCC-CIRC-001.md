---
card_id: PCC-CIRC-001
title: PCC 阶段循环复苏目标与休克分型
version: '1.0'
module: PCC
topic: PCC 循环
task_type: decision
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
- 失血性休克战伤伤员
related_cards:
- CIRC-001
- CIRC-007
- CIRC-013
- PCC-HEM-001
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: CIRCULATION AND RESUSCITATION - PCC
  locator: p.17-19 Background, Table 5
  quote: The goals are a return to a normal level of consciousness (LOC), increase and stabilization of systolic blood pressure
    at 100-110 mm Hg... Differentiate between transient responder, non-responder, and refractory shock.
---

# PCC 阶段循环复苏目标与休克分型

## 1. 核心问题

PCC 阶段循环复苏的稳定目标是什么,如何分辨瞬时反应、不反应与难治性休克


## 2. 输出目标

让模型输出 PCC 复苏终点 (LOC 恢复, SBP 100-110) 与 3 类休克反应的鉴别


## 3. 适用场景与边界

**适用场景**:
- PCC Role 1b/1c

**前置条件**:
- 已建立 IV/IO 通路
- 已开始血制品复苏

**不覆盖范围**:
- 不覆盖 TCCC 阶段早期复苏目标


## 4. 触发与识别

**触发条件**:
- 进入 PCC 持续复苏阶段


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 复苏目标: 意识水平恢复,SBP 稳定在 100-110 mmHg,生命体征稳定 | immediate | PCC 整个复苏期间 | 持续 | PCC 比 TCCC 提高目标 SBP |
| 2 | 持续判别 transient responder / non-responder / refractory shock 三类 | high | Role 1b 及以上 | 每次输血/输液后复评 | CMC/CPP 必备技能 |
| 3 | 复评后申请血液 / 血浆 / 装备的再补给 | high | 复苏需求超过现有储备 | 尽早 | speedball 等非常规补给手段 |


## 6. 决策点

**1.**
- 如果(condition):输血后短暂改善又恶化 (transient responder)
- 则(next_action):排查持续出血源,继续输血并申请补给
- 依据(rationale):提示存在未控制的出血
- 分支类型:`if_then`

**2.**
- 如果(condition):输血后无任何改善 (non-responder)
- 则(next_action):高度怀疑致命未控制的腹腔/胸腔/盆腔出血
- 依据(rationale):需要立即升级或后送
- 分支类型:`escalation`


## 7. 复评 / 终点 / 禁忌 / 错误

**处置终点**:
- LOC 恢复
- SBP 100-110 mmHg 稳定
- 尿量 ≥0.5 ml/kg/h

**常见错误**:
- 用 TCCC 的 SBP 80-90 mmHg 目标管理 PCC
- 未区分 transient/non-responder 而盲目输液


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `CIRCULATION AND RESUSCITATION - PCC`
  - 位置: `p.17-19 Background, Table 5`
  - 原文引用:
    > The goals are a return to a normal level of consciousness (LOC), increase and stabilization of systolic blood pressure at 100-110 mm Hg... Differentiate between transient responder, non-responder, and refractory shock.


## 9. 评分要点(LLM 评测)

- 是否提到目标 SBP 100-110 mmHg
- 是否提到三类休克反应
- 是否提到尿量目标


## 10. 备注

新增依据: PCC CPG 增补; 与 TCCC CIRC-013 互补

