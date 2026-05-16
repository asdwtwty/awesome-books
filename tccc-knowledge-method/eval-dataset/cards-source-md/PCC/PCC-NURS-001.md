---
card_id: PCC-NURS-001
title: PCC 阶段护理与伤口换药频率体系
version: '1.0'
module: PCC
topic: PCC 护理
task_type: procedure
training_use:
- fact_qa
- case_qa
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
- 卧床战伤伤员
related_cards:
- PCC-PRIN-002
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: WOUND CARE AND NURSING - PCC
  locator: p.43-45 Table 17
  quote: 'Nutrition: Every 4-6 hours; Hygiene: Every 24 hours; Deep Vein Thrombosis Prevention: Every 1-2 hours; Head Injury
    Serial Neuro Exams: every 8-12 hours.'
---

# PCC 阶段护理与伤口换药频率体系

## 1. 核心问题

PCC 阶段哪些护理项目需要按多长频率执行


## 2. 输出目标

让模型输出 PCC 营养/卫生/排便/DVT 预防/神经检查的频率与最低-更好-最佳分级


## 3. 适用场景与边界

**适用场景**:
- Role 1b/1c

**前置条件**:
- 伤员处于 PCC > 4 小时

**不覆盖范围**:
- 不覆盖伤口具体止血操作


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 营养: 每 4-6 小时给清醒伤员口服食物水,无意识者考虑管饲 | high | 无消化道损伤 | 每 4-6 小时 | minimum: 鼓励进食; better: MRE 蛋白粉; best: 商品化管饲制品 |
| 2 | 卫生: 每 24 小时清洁面部/腋下/腹股沟 | high | 卧床伤员 | 每 24 小时 | minimum: 温水皂洗; best: 氯己定湿巾 |
| 3 | DVT 预防: 每 1-2 小时按摩下肢或加弹力袜/机械加压 | high | 卧床 > 数小时 | 每 1-2 小时 | 注意患肢避免按压伤口 |
| 4 | 神经检查 (头颅伤者): 瞳孔/GCS/意识每 8-12 小时一次,MACE Exam 评估 | high | 存在头颅伤 | 每 8-12 小时 | PCC CPG 第 17 页 |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**文书记录要求**:
- 所有护理操作记录到 PCC Flowsheet


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `WOUND CARE AND NURSING - PCC`
  - 位置: `p.43-45 Table 17`
  - 原文引用:
    > Nutrition: Every 4-6 hours; Hygiene: Every 24 hours; Deep Vein Thrombosis Prevention: Every 1-2 hours; Head Injury Serial Neuro Exams: every 8-12 hours.


## 9. 评分要点(LLM 评测)

- 是否提到营养 4-6 小时频率
- 是否提到卫生 24 小时一次
- 是否提到 DVT 预防 1-2 小时一次
- 是否提到神经检查 8-12 小时一次 (头颅伤)


## 10. 备注

新增依据: PCC CPG; TCCC 卡片清单中未覆盖长程护理

