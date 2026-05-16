---
card_id: PCC-HEM-001
title: PCC 阶段大出血控制的角色分级要求 (TCCC-ASM 至 TCCC-CPP)
version: '1.0'
module: PCC
topic: PCC 大出血
task_type: decision
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
- HEM-005
- HEM-019
- HEM-021
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: MASSIVE HEMORRHAGE - PCC
  locator: p.11-12 Table 2
  quote: Role 1a Re-assess all prior MARCH interventions. Role 1b Assess using ultrasound (if available) including Extended
    Focused Assessment with Sonography in Trauma. Role 1c Convert to type-specific blood replacement, if testing available.
    Establish Foley catheter with goal Urine Output (UOP) of > ½ ml/kg per hour.
---

# PCC 阶段大出血控制的角色分级要求 (TCCC-ASM 至 TCCC-CPP)

## 1. 核心问题

PCC 阶段不同 TCCC 角色 (ASM/CLS/CMC/CPP) 在大出血控制上的递进任务是什么


## 2. 输出目标

让模型输出 PCC 4 级 TCCC 角色在大出血上的递进职责


## 3. 适用场景与边界

**适用场景**:
- Role 1a/1b/1c PCC 环境

**前置条件**:
- 已完成 TCCC 大出血基础处置

**不覆盖范围**:
- 不覆盖止血带操作细节 (见 HEM-001 至 HEM-005)


## 4. 触发与识别

**触发条件**:
- 处于 PCC 状态
- 存在或曾经存在致命性出血


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | All Personnel: 完成基础 TCCC 大出血处置 | immediate | PCC 启动 | 立即 | 前置基础 |
| 2 | Role 1a (ASM/CLS): 重新识别撤离/拖动后可能新发的出血 | high | Role 1a (<1 小时) | 持续 | 出血可能在转运中重启 |
| 3 | Role 1b (CMC): 用超声 (eFAST/CVP) 评估容量与休克 | high | Role 1b (1-4 小时), 设备可用 | 尽早 | 区分低血容量 vs 难治性休克 |
| 4 | Role 1c (CPP): 在可做血型测定时转换为同型血制品 | high | Role 1c (>4 小时), 实验室可用 | 条件允许时 | 保留低滴度 O 型全血给紧急情况 |
| 5 | Role 1c (CPP): 留置 Foley 导尿管,目标尿量 >0.5 ml/kg/h | high | Role 1c | 尽早 | 尿量是 PCC 唯一稳定的器官灌注指标 |


## 6. 决策点

**1.**
- 如果(condition):进入 Role 1b 且设备允许
- 则(next_action):用 eFAST 确认/排除腹腔出血
- 依据(rationale):区分低血容量与难治性休克决定后续资源
- 分支类型:`escalation`


## 7. 复评 / 终点 / 禁忌 / 错误

**文书记录要求**:
- PCC Flowsheet 上记录所有干预
- 持续记录尿量


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `MASSIVE HEMORRHAGE - PCC`
  - 位置: `p.11-12 Table 2`
  - 原文引用:
    > Role 1a Re-assess all prior MARCH interventions. Role 1b Assess using ultrasound (if available) including Extended Focused Assessment with Sonography in Trauma. Role 1c Convert to type-specific blood replacement, if testing available. Establish Foley catheter with goal Urine Output (UOP) of > ½ ml/kg per hour.


## 9. 评分要点(LLM 评测)

- 是否提到 Role 1a 重新评估出血
- 是否提到 Role 1b 用超声 + eFAST
- 是否提到 Role 1c 转换同型血
- 是否提到 Foley 尿量目标 >0.5 ml/kg/h


## 10. 备注

新增依据: PCC CPG 增补 (TCCC 卡片清单未覆盖角色分级)

