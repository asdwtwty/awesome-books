---
card_id: ATP-EYE-001
title: '眼外伤分型: 眼睑切割 / 眼球切割 / 强光烧伤识别'
version: '1.0'
module: ATP
topic: 眼外伤
task_type: recognition
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
- EYE-001
- EYE-002
- EYE-003
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 10 Eye Trauma
  locator: 10-1 to 10-2, p.97
  quote: Cuts of the eyelids can appear to be very serious, but if the eyeball is not involved, a person's vision usually
    will not be damaged. However, lacerations (cuts) of the eyeball can cause permanent damage or loss of sight.
---

# 眼外伤分型: 眼睑切割 / 眼球切割 / 强光烧伤识别

## 1. 核心问题

如何区分眼睑切割、眼球切割与强光烧伤这三类眼外伤


## 2. 输出目标

让模型输出三类眼外伤的识别要点 + 视力影响差异


## 3. 适用场景与边界

**适用场景**:
- 战术现场

**前置条件**:
- 眼周明显外伤

**不覆盖范围**:
- 不覆盖具体眼罩放置 (见 EYE-002)


## 4. 触发与识别

**识别要点**:
- 眼睑切割: 看似严重但不累及眼球时通常视力不受影响
- 眼球切割: 可造成永久损伤或失明
- 强光烧伤: 红外线/日蚀光/激光暴露后
- 视力突然下降伴疼痛


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 评估视力 (能否数手指 / 看见光线方向) | immediate | 怀疑眼外伤 | 立即 | 决定后送优先级 |
| 2 | 区分三类: 仅眼睑伤 / 累及眼球 / 强光暴露 | immediate | 完成视力评估 | 立即 | 三类处置不同 |


## 6. 决策点

**1.**
- 如果(condition):怀疑眼球切割或穿通
- 则(next_action):硬质眼罩保护并紧急后送
- 依据(rationale):视力可永久丧失
- 分支类型:`escalation`

**2.**
- 如果(condition):仅眼睑伤未累及眼球
- 则(next_action):敷料覆盖,继续按 MARCH 处置
- 依据(rationale):视力通常不受影响
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 把仅眼睑切割视为视力威胁
- 忽略激光暴露伤


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 10 Eye Trauma`
  - 位置: `10-1 to 10-2, p.97`
  - 原文引用:
    > Cuts of the eyelids can appear to be very serious, but if the eyeball is not involved, a person's vision usually will not be damaged. However, lacerations (cuts) of the eyeball can cause permanent damage or loss of sight.


## 9. 评分要点(LLM 评测)

- 是否提到三类区分
- 是否提到先评估视力
- 是否提到激光/日蚀强光暴露


## 10. 备注

新增依据: ATP Chapter 10; TCCC EYE 模块仅 4 张未覆盖分型识别

