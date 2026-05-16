---
card_id: PCC-PRIN-001
title: PCC 阶段总体目标与团队职责分配
version: '1.0'
module: PCC
topic: PCC 原则与团队
task_type: decision
training_use:
- fact_qa
- case_qa
- structured_decision
- retrieval
difficulty: basic
applicable_phase:
- prolonged_casualty_care
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 成人战伤伤员
related_cards:
- PCC-PRIN-002
- PCC-MASCAL-001
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: PCC PRINCIPLES
  locator: p.6-7 Steps 1-2
  quote: Perform initial lifesaving care using TCCC guidelines and continue resuscitation. Delineate roles and responsibilities,
    including naming a team leader.
---

# PCC 阶段总体目标与团队职责分配

## 1. 核心问题

进入 PCC 阶段后,救护团队的总体目标是什么、如何分工


## 2. 输出目标

让模型输出 PCC 的核心目标 (尽快脱离 PCC) 与团队领队负责制


## 3. 适用场景与边界

**适用场景**:
- 远程或荒漠环境
- 撤运能力或容量超限

**前置条件**:
- TCCC 初救已完成
- 短时间内无法后送至 Role 2/3

**不覆盖范围**:
- 不覆盖具体处置步骤
- 不覆盖 MASCAL 分诊细节


## 4. 触发与识别

**触发条件**:
- 撤运需求超过当前能力
- 处于伤后 1-4 小时及以上


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 继续按 TCCC 完成初步抢救并保持复苏 | immediate | 进入 PCC 阶段 | 持续 | PCC 的基础是 TCCC 熟练度 |
| 2 | 明确角色与责任,指定一名团队领队管理整体临床决策 | immediate | 至少 2 名以上施救者在场 | 尽快 | 助手专注高强度任务 |
| 3 | 牢记 PCC 的首要目标是尽快脱离 PCC | high | 整个 PCC 期间 | 持续 | 原文: 'the primary goal in PCC is to get out of PCC' |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**处置终点**:
- 伤员被后送
- 进入更高一级救治

**常见错误**:
- 把 PCC 当作终点而非桥梁
- 无人统筹指挥导致复苏混乱


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `PCC PRINCIPLES`
  - 位置: `p.6-7 Steps 1-2`
  - 原文引用:
    > Perform initial lifesaving care using TCCC guidelines and continue resuscitation. Delineate roles and responsibilities, including naming a team leader.


## 9. 评分要点(LLM 评测)

- 是否提到延续 TCCC 复苏
- 是否提到指定团队领队
- 是否提到首要目标是脱离 PCC


## 10. 备注

PCC 总纲第一卡; 新增依据: PCC CPG 增补

