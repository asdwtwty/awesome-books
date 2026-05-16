---
card_id: PCC-COMM-001
title: PCC 阶段远程会诊与文书 (DD Form 1380 + PCC Flowsheet)
version: '1.0'
module: PCC
topic: PCC 通信文书
task_type: documentation
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
- EVAC-004
- PCC-PRIN-002
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: COMMUNICATION AND DOCUMENTATION - PCC
  locator: p.20-21 Table 6
  quote: Document casualty information on the DD Form 1380 TCCC Card and ensure proper placement of that card on the casualty,
    in accordance with DHA-PI 6040.01. Initiate scripted teleconsultation.
---

# PCC 阶段远程会诊与文书 (DD Form 1380 + PCC Flowsheet)

## 1. 核心问题

PCC 阶段需要做哪些通信和文书工作


## 2. 输出目标

让模型输出与伤员/战术指挥/医疗后台的三类沟通要求 + 标准文书表


## 3. 适用场景与边界

**适用场景**:
- 所有 PCC 角色

**前置条件**:
- 伤员处于 PCC > 数小时

**不覆盖范围**:
- 不覆盖 TACEVAC 现场交接


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 与伤员沟通: 鼓励、安抚、解释处置 | high | 伤员清醒 | 持续 | 提高配合度,降低焦虑 |
| 2 | 与战术指挥沟通: 报告伤情、撤运需求、补给请求 | immediate | PCC 启动 | 尽快并持续 | 战术决策依赖此信息 |
| 3 | 发起 teleconsultation 远程会诊,使用预制脚本 | high | 通信条件允许 | 尽早 | teleconsultation 是 PCC 关键支撑 |
| 4 | 在 DD Form 1380 (TCCC 卡) 上记录全部干预,按 DHA-PI 6040.01 放置于伤员 | high | 整个 PCC 期间 | 持续 | 卡片必须随伤员转运 |
| 5 | 在 PCC Flowsheet 上记录生命体征趋势、用药、出入量 | high | Role 1b/1c | 每次复评后 | PCC 专用流程表 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**文书记录要求**:
- DD Form 1380 TCCC Card
- PCC Flowsheet


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `COMMUNICATION AND DOCUMENTATION - PCC`
  - 位置: `p.20-21 Table 6`
  - 原文引用:
    > Document casualty information on the DD Form 1380 TCCC Card and ensure proper placement of that card on the casualty, in accordance with DHA-PI 6040.01. Initiate scripted teleconsultation.


## 9. 评分要点(LLM 评测)

- 是否提到三类沟通对象 (伤员/战术/医疗)
- 是否提到 teleconsultation 预制脚本
- 是否提到 DD Form 1380
- 是否提到 PCC Flowsheet


## 10. 备注

新增依据: PCC CPG; 补充 TCCC EVAC-004 在 PCC 长程场景下的延伸

