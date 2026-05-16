---
card_id: PCC-HYP-001
title: PCC 阶段长时程低体温预防 (>10 小时加温毯更换)
version: '1.0'
module: PCC
topic: PCC 低体温
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
- 成人战伤伤员
related_cards:
- HYP-004
- HYP-005
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: HYPOTHERMIA - PCC
  locator: p.22-23
  quote: Role 1c Continue and/or initiate the Role 1a/Role 1b phases as detailed above. Replace ready-heat-blanket when using
    >10 hours.
---

# PCC 阶段长时程低体温预防 (>10 小时加温毯更换)

## 1. 核心问题

PCC 阶段长时程低体温预防与 TCCC 阶段的关键差别是什么


## 2. 输出目标

让模型输出 ready-heat-blanket 使用 >10 小时需更换 + 持续保温的延伸要求


## 3. 适用场景与边界

**适用场景**:
- Role 1c PCC > 4 小时

**前置条件**:
- TCCC 阶段已启动低体温预防

**不覆盖范围**:
- 不覆盖 TCCC 阶段初始保温步骤 (见 HYP-001 至 HYP-009)


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | Role 1c: 持续/重启 1a 与 1b 的所有保温措施 | high | 进入 Role 1c | 持续 | 确保前置措施仍在位 |
| 2 | ready-heat-blanket 使用超过 10 小时时更换 | high | 已使用 ≥10 小时 | 10 小时整点 | 化学加温毯有效时长上限 |
| 3 | 在撤运平台上保护伤员避免风雨暴露 | high | Role 1b 撤运平台 | 持续 | 对流和蒸发会持续耗热 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 误以为 ready-heat-blanket 可一直用
- 撤运平台上忽视风雨暴露


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `HYPOTHERMIA - PCC`
  - 位置: `p.22-23`
  - 原文引用:
    > Role 1c Continue and/or initiate the Role 1a/Role 1b phases as detailed above. Replace ready-heat-blanket when using >10 hours.


## 9. 评分要点(LLM 评测)

- 是否提到 ready-heat-blanket >10 小时需更换
- 是否提到撤运平台上防风雨


## 10. 备注

新增依据: PCC CPG 长时程化措施 (TCCC HYP-001~009 不覆盖 >10 小时)

