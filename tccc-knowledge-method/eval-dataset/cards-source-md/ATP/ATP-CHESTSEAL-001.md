---
card_id: ATP-CHESTSEAL-001
title: 胸部贯通伤多个伤口的处置原则
version: '1.0'
module: ATP
topic: 呼吸
task_type: decision
training_use:
- fact_qa
- case_qa
- retrieval
difficulty: intermediate
applicable_phase:
- tactical_field_care
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 成人战伤伤员
related_cards:
- RESP-013
- RESP-015
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 6 Respiration and Breathing Control
  locator: 6-26, p.77
  quote: If unsure that the wound has penetrated the chest wall completely, treat the wound as though it were an open chest
    wound. If multiple wounds are found, treat as soon as they are discovered.
---

# 胸部贯通伤多个伤口的处置原则

## 1. 核心问题

发现多个开放性胸壁伤口时如何处置


## 2. 输出目标

让模型输出'发现一个就立即处理一个'+ 张力性气胸恶化时的 burp 路径


## 3. 适用场景与边界

**适用场景**:
- TFC 胸部贯通伤

**前置条件**:
- 已确认开放性胸壁伤

**不覆盖范围**:
- 不覆盖针刺减压具体技术


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 发现一个开放胸伤立即用胸封覆盖,不等所有伤口暴露 | immediate | 首次发现开放胸伤 | 立即 | ATP §6-26 |
| 2 | 不能确定伤口是否贯穿胸壁时,按开放胸伤同等处理 | immediate | 贯穿不确定 | 立即 | 保守原则 |
| 3 | 贴胸封后伤员恶化,先 burp (放气) 或临时移除敷料 | immediate | 贴胸封后症状加重 | 立即 | 怀疑张力性气胸 |


## 6. 决策点

**1.**
- 如果(condition):贯穿性不确定
- 则(next_action):按开放胸伤处理
- 依据(rationale):宁可保守不可漏诊
- 分支类型:`if_then`

**2.**
- 如果(condition):胸封后伤员恶化
- 则(next_action):Burp 胸封,必要时针刺减压
- 依据(rationale):张力性气胸进展
- 分支类型:`escalation`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 全部伤口找完才处理
- 胸封后忽略恶化征象


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 6 Respiration and Breathing Control`
  - 位置: `6-26, p.77`
  - 原文引用:
    > If unsure that the wound has penetrated the chest wall completely, treat the wound as though it were an open chest wound. If multiple wounds are found, treat as soon as they are discovered.


## 9. 评分要点(LLM 评测)

- 是否提到一个发现一个处理一个
- 是否提到不确定时按开放胸伤处理
- 是否提到 burp 或临时移除


## 10. 备注

新增依据: ATP §6-26; TCCC RESP-013 不覆盖多个伤口和不确定贯穿

