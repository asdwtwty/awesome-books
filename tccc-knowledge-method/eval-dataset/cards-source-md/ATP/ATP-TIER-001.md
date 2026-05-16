---
card_id: ATP-TIER-001
title: 'ATP 4-02.11 医疗梯次职责: All Service Members / CLS / Combat Medic'
version: '1.0'
module: ATP
topic: 医疗梯次
task_type: decision
training_use:
- fact_qa
- structured_decision
- retrieval
difficulty: basic
applicable_phase:
- care_under_threat
- tactical_field_care
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 陆军全员
related_cards:
- PHASE-001
- PHASE-004
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 1 Medical Tier Responsibilities
  locator: Table 1-1, p.2
  quote: 'All Service Members - Care Under Fire: Ensure scene safety. Move the casualty to safety. Identify and control life-threatening
    bleeding. Combat Lifesaver - Care Under Fire: Suppress hostile fire to minimize the risk of injury to personnel.'
---

# ATP 4-02.11 医疗梯次职责: All Service Members / CLS / Combat Medic

## 1. 核心问题

ATP 4-02.11 中三类施救梯次 (全体兵员 / CLS / Combat Medic) 在 CUF 与 TFC 的具体职责是什么


## 2. 输出目标

让模型输出三梯次按 CUF/TFC 分阶段的职责清单


## 3. 适用场景与边界

**适用场景**:
- 野战行动 CUF/TFC

**前置条件**:
- 战场环境

**不覆盖范围**:
- 不覆盖 TACEVAC 阶段升级处置


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 全体兵员 (CUF): 确保现场安全 / 把伤员转移到掩体 / 识别并控制致命出血 | immediate | CUF | 立即 | ATP Table 1-1 |
| 2 | 全体兵员 (TFC): 快速伤员评估 / 按治疗规程处置 / 按单位 SOP 求助 | immediate | TFC | 进入 TFC | 受过基础急救训练即可 |
| 3 | CLS (CUF): 压制敌火力 / 减少二次伤害 / 协助自助互助 / 维持安全和态势感知 | immediate | CUF + CLS 在场 | 立即 | CLS 是非医务但接受过加强训练的士兵 |
| 4 | CLS (TFC): 完成伤员评估 / 按规程处置 / 配合 Combat Medic | high | TFC | 持续 | 强化版基础急救 |
| 5 | Combat Medic: 在 CUF 与 TFC 中执行 TCCC 五项关键救命技能 | immediate | TFC 主救者 | 全程 | ATP §3-77 引用 CoTCCC 五项 |


## 6. 决策点

**1.**
- 如果(condition):现场仅有非医务兵员
- 则(next_action):执行 All Service Members 梯次任务,寻求 CLS/Medic 援助
- 依据(rationale):梯次决定可执行范围
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

_(暂无)_


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 1 Medical Tier Responsibilities`
  - 位置: `Table 1-1, p.2`
  - 原文引用:
    > All Service Members - Care Under Fire: Ensure scene safety. Move the casualty to safety. Identify and control life-threatening bleeding. Combat Lifesaver - Care Under Fire: Suppress hostile fire to minimize the risk of injury to personnel.


## 9. 评分要点(LLM 评测)

- 是否提到三梯次划分
- 是否提到全体兵员 CUF 三大任务
- 是否提到 CLS 在 CUF 中压制火力角色
- 是否提到 Combat Medic 是 TFC 主救者


## 10. 备注

新增依据: ATP 4-02.11 Table 1-1; TCCC 不提供这种梯次详细分工

