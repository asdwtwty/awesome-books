---
card_id: PCC-SPLINT-001
title: PCC 阶段长时程夹板与担架填充的分级要求
version: '1.0'
module: PCC
topic: PCC 骨折与长时程固定
task_type: procedure
training_use:
- fact_qa
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
- 四肢骨折伤员
related_cards:
- MSK-001
- MSK-002
- MSK-003
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: SPLINTING AND FRACTURE MANAGEMENT - PCC
  locator: p.46 Table 18
  quote: 'Litter Padding: Minimum - Excess uniforms or other textiles; Better/Best - Blankets or military sleep pad. Splint
    Placement: Minimum - Improvised splints; Better/Best - Commercial splinting device. Re-check all pulses after splint placement.'
---

# PCC 阶段长时程夹板与担架填充的分级要求

## 1. 核心问题

PCC 阶段对于担架填充和夹板的分级最低-更好-最佳标准是什么


## 2. 输出目标

让模型输出担架填充与夹板装备的分级 + 固定后必须复查脉搏


## 3. 适用场景与边界

**适用场景**:
- PCC > 4 小时长程转运

**前置条件**:
- 已识别骨折

**不覆盖范围**:
- 不覆盖 TCCC 阶段初次夹板放置 (见 MSK-001~003)


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 担架填充: minimum 多余军服; better 毛毯或睡垫; best 毛毯或军用睡垫 | high | 卧担架超过数小时 | 立即 | 防压疮和长时不适 |
| 2 | 夹板: minimum 临时性 (木板/金属板); better/best 商品化 (SAM splint 等) | high | 存在四肢骨折 | 立即 | PCC 长程更重视固定可靠性 |
| 3 | 夹板放置后必须复查全部远端脉搏 | immediate | 完成固定 | 立即 | 与 MSK-002 衔接 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**复评要点**:
- 远端脉搏
- 皮肤温度颜色

**常见错误**:
- PCC 长程仍使用紧急临时夹板未升级
- 固定后未复查脉搏


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `SPLINTING AND FRACTURE MANAGEMENT - PCC`
  - 位置: `p.46 Table 18`
  - 原文引用:
    > Litter Padding: Minimum - Excess uniforms or other textiles; Better/Best - Blankets or military sleep pad. Splint Placement: Minimum - Improvised splints; Better/Best - Commercial splinting device. Re-check all pulses after splint placement.


## 9. 评分要点(LLM 评测)

- 是否提到担架填充分级
- 是否提到 SAM splint
- 是否提到固定后复查脉搏


## 10. 备注

新增依据: PCC CPG 长程固定;扩展 TCCC MSK

