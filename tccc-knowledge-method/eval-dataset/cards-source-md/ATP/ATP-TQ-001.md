---
card_id: ATP-TQ-001
title: 止血带应用时间窗 (失血致死最短 3 分钟,目标 1 分钟内上 TQ)
version: '1.0'
module: ATP
topic: 大出血控制
task_type: recognition
training_use:
- fact_qa
- retrieval
- judge_eval
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
- 成人战伤伤员
related_cards:
- HEM-001
- HEM-002
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 3 Fundamentals of TCCC
  locator: 3-75, p.37
  quote: A hasty TQ should be applied promptly and tightly to stop the bleeding (ideally within one minute)... a casualty
    to succumb to exsanguination in as little as three minutes.
---

# 止血带应用时间窗 (失血致死最短 3 分钟,目标 1 分钟内上 TQ)

## 1. 核心问题

为什么 ATP 4-02.11 强调止血带必须在 1 分钟内应用


## 2. 输出目标

让模型输出失血致死时间窗 + 1 分钟应用目标的依据


## 3. 适用场景与边界

**适用场景**:
- 战场致命四肢出血

**前置条件**:
- 确认致命四肢出血

**不覆盖范围**:
- 不覆盖具体止血带操作技术 (见 HEM-001~005)


## 4. 触发与识别

**触发条件**:
- 可见喷射性或大量出血

**识别要点**:
- 动脉性喷射出血
- 短时间内浸透多层敷料
- 创伤性截肢


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 理想在 1 分钟内紧急上止血带 | immediate | 致命四肢出血确认 | <1 分钟 | ATP §3-75 目标 |
| 2 | 认识到伤员在 3 分钟内即可因失血死亡 | immediate | 训练与决策时 | 认知层面 | ATP §3-75: as little as 3 minutes |


## 6. 决策点

_(暂无)_


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 把 1 分钟目标当成普通急救用时
- 忽略 3 分钟致死时间窗


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 3 Fundamentals of TCCC`
  - 位置: `3-75, p.37`
  - 原文引用:
    > A hasty TQ should be applied promptly and tightly to stop the bleeding (ideally within one minute)... a casualty to succumb to exsanguination in as little as three minutes.


## 9. 评分要点(LLM 评测)

- 是否提到 1 分钟应用目标
- 是否提到 3 分钟致死风险
- 是否提到致命四肢出血是 TQ 适应证


## 10. 备注

新增依据: ATP §3-75; TCCC 仅说 immediate 但 ATP 给定时窗

