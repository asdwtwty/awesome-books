---
card_id: PCC-PRIN-002
title: PCC 全身体格检查与生命体征趋势记录
version: '1.0'
module: PCC
topic: PCC 原则与团队
task_type: procedure
training_use:
- fact_qa
- case_qa
- structured_decision
- retrieval
difficulty: intermediate
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
- PCC-PRIN-001
- PCC-COMM-001
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: PCC PRINCIPLES
  locator: p.7 Steps 3-5
  quote: Perform comprehensive physical exam and detailed history with problem list and care plan. Record and trend vital
    signs.
---

# PCC 全身体格检查与生命体征趋势记录

## 1. 核心问题

PCC 阶段如何完成详细体检和生命体征趋势化记录


## 2. 输出目标

让模型输出 PCC 的标准化检查 + 持续趋势化


## 3. 适用场景与边界

**适用场景**:
- Role 1a-1c PCC 现场

**前置条件**:
- 伤员已初步稳定

**不覆盖范围**:
- 不覆盖具体器官处置


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 完成详细头到脚体检 + 完整问诊,形成 problem list 与 care plan | high | 首次稳定后 | 尽快 | PCC CPG 第 3 步 |
| 2 | 建立专用趋势表,从最早一组生命体征开始记录,定期复测 | immediate | 整个 PCC 期间 | 1-2 小时一次 | 稳定后可延长至 4 小时 |
| 3 | 尽快发起 teleconsultation (远程会诊),按预制模板汇报 | high | 通信条件允许 | 尽早 | PCC CPG 第 5 步 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**复评要点**:
- 心率 / 呼吸 / SpO2 / 血压 / 体温 / AVPU

**文书记录要求**:
- PCC Flowsheet
- 趋势化生命体征图表


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `PCC PRINCIPLES`
  - 位置: `p.7 Steps 3-5`
  - 原文引用:
    > Perform comprehensive physical exam and detailed history with problem list and care plan. Record and trend vital signs.


## 9. 评分要点(LLM 评测)

- 是否提到完整体检 + 病史
- 是否提到问题清单与照护计划
- 是否提到生命体征趋势化记录
- 是否提到尽早 teleconsultation


## 10. 备注

PCC 监测原则,新增依据: PCC CPG 增补

