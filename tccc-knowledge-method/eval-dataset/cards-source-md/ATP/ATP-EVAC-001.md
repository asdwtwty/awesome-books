---
card_id: ATP-EVAC-001
title: '陆军伤员撤运四级分类: Urgent / Priority / Routine / RTD'
version: '1.0'
module: ATP
topic: 撤运
task_type: triage
training_use:
- fact_qa
- case_qa
- structured_decision
- retrieval
difficulty: basic
applicable_phase:
- tactical_field_care
- tacevac
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 全部伤员
related_cards:
- TRIAGE-002
- TRIAGE-003
- PCC-MASCAL-001
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 1 Casualty Reporting
  locator: 1-55, p.12
  quote: Casualties are taken to the CCP for classification of injury type (urgent, priority, routine, or return to duty),
    evacuation, and integration into the medical evacuation system.
---

# 陆军伤员撤运四级分类: Urgent / Priority / Routine / RTD

## 1. 核心问题

陆军 ATP 4-02.11 中伤员撤运分四类是什么


## 2. 输出目标

让模型输出 Urgent/Priority/Routine/RTD 四类的定义


## 3. 适用场景与边界

**适用场景**:
- 排连级现场分诊

**前置条件**:
- 完成初步评估

**不覆盖范围**:
- 不覆盖 MASCAL 颜色编码 (immediate/delayed/minimal/expectant)


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | Urgent: 需 1 小时内后送以挽救生命/肢体/视力 | immediate | 立即危及生命 | ≤1 小时 | 如失血休克未控、张力性气胸 |
| 2 | Priority: 需 4 小时内后送防止恶化 | high | 暂稳定但快速恶化风险 | ≤4 小时 | 如稳定的烧伤需补液 |
| 3 | Routine: 24 小时内后送即可 | routine | 稳定无快速恶化风险 | ≤24 小时 | 如简单四肢骨折 |
| 4 | Return to Duty (RTD): 简单处置后即可归队 | routine | 轻伤无需后送 | 现场处理后 | 陆军特有分类 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 把 Urgent 与 immediate (颜色卡) 混淆
- 忽视 RTD 分类导致无关人员后送占资源

**文书记录要求**:
- 在 DD Form 1380 上记录分类
- 持续报告至 Battalion S-1


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 1 Casualty Reporting`
  - 位置: `1-55, p.12`
  - 原文引用:
    > Casualties are taken to the CCP for classification of injury type (urgent, priority, routine, or return to duty), evacuation, and integration into the medical evacuation system.


## 9. 评分要点(LLM 评测)

- 是否提到 4 类 (Urgent/Priority/Routine/RTD)
- 是否提到 Urgent 1 小时窗
- 是否提到 Priority 4 小时
- 是否提到 Routine 24 小时


## 10. 备注

新增依据: ATP 1-55; 与 PCC MASCAL 颜色卡片互补

