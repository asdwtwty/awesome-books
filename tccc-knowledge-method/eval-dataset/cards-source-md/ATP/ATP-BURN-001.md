---
card_id: ATP-BURN-001
title: '烧伤面积速估手法: 手掌 1% + 九分法'
version: '1.0'
module: ATP
topic: 烧伤
task_type: procedure
training_use:
- fact_qa
- case_qa
- retrieval
difficulty: basic
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
- BURN-004
- BURN-007
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 12 Burns
  locator: 12-5, p.117
  quote: the size of the casualty's palm of the hand represents approximately 1 percent of the burned area. When estimating,
    it is easiest to round up to the nearest 10 percent.
---

# 烧伤面积速估手法: 手掌 1% + 九分法

## 1. 核心问题

战场如何快速估算烧伤面积


## 2. 输出目标

让模型输出手掌法 (≈1%) + Rule of Nines + 取整到 10% 的实操手法


## 3. 适用场景与边界

**适用场景**:
- TFC 烧伤评估

**前置条件**:
- 明显烧伤

**不覆盖范围**:
- 不覆盖儿童九分法变体


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 用伤员手掌作为 ≈1% TBSA 的估算尺度 | high | 小面积或散在烧伤 | 立即 | ATP §12-5 通用法 |
| 2 | 用 Rule of Nines 估算大面积,然后取整到最接近的 10% | high | 大面积烧伤 | 立即 | 战场快估,精度容差换速度 |
| 3 | 若仅前/后侧的一半受累,取该区域值的一半 | high | 半侧受累 | 立即 | 举例: 半个躯干前侧 9% |


## 6. 决策点

**1.**
- 如果(condition):烧伤面积越大
- 则(next_action):更强化低体温预防
- 依据(rationale):皮肤丧失加重热量丢失
- 分支类型:`escalation`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 战场上追求精确 % 浪费时间
- 忽视半侧受累的折半计算


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 12 Burns`
  - 位置: `12-5, p.117`
  - 原文引用:
    > the size of the casualty's palm of the hand represents approximately 1 percent of the burned area. When estimating, it is easiest to round up to the nearest 10 percent.


## 9. 评分要点(LLM 评测)

- 是否提到手掌 ≈1%
- 是否提到 Rule of Nines
- 是否提到取整到最接近的 10%
- 是否提到面积越大越要防低体温


## 10. 备注

新增依据: ATP §12-5; TCCC BURN-004 仅说 Rule of Nines 未给战场速估手掌法

