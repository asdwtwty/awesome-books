---
card_id: ATP-PRESSDRES-001
title: 加压敷料复评要点 (远端脉搏 / 皮肤温度 / 颜色)
version: '1.0'
module: ATP
topic: 循环
task_type: reassessment
training_use:
- fact_qa
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
- 四肢加压敷料伤员
related_cards:
- HEM-018
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 7 Circulation Control
  locator: 7-22, p.87
  quote: If the skin below the bandage is cool, bluish, numb, or if the distal pulse is absent, these may be signs that the
    bandage is applied too tightly.
---

# 加压敷料复评要点 (远端脉搏 / 皮肤温度 / 颜色)

## 1. 核心问题

加压敷料应用后必须如何复评


## 2. 输出目标

让模型输出 CLS 复评 4 项: 出血是否停止 / 远端脉搏 / 皮肤温度 / 颜色


## 3. 适用场景与边界

**适用场景**:
- TFC 与 TACEVAC

**前置条件**:
- 已应用加压敷料

**不覆盖范围**:
- 不覆盖止血带复评 (见 HEM-018)


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 复评是否仍有活动性出血 | immediate | 应用敷料后 | 立即并周期性 | 出血未止则升级 |
| 2 | 触诊敷料远端脉搏 | immediate | 应用敷料后 | 立即 | 脉搏消失提示包扎过紧 |
| 3 | 评估远端皮肤温度颜色,凉/紫/麻木提示血供受阻 | immediate | 应用敷料后 | 立即 | ATP §7-22 |


## 6. 决策点

**1.**
- 如果(condition):远端脉搏消失或皮肤变冷/紫/麻木
- 则(next_action):松开敷料并安全重新缠绕
- 依据(rationale):包扎过紧会致缺血
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

**复评要点**:
- 出血
- 远端脉搏
- 皮肤温度
- 皮肤颜色

**常见错误**:
- 只看是否止血未查远端血供
- 皮肤颜色变化误判


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 7 Circulation Control`
  - 位置: `7-22, p.87`
  - 原文引用:
    > If the skin below the bandage is cool, bluish, numb, or if the distal pulse is absent, these may be signs that the bandage is applied too tightly.


## 9. 评分要点(LLM 评测)

- 是否提到复评 4 要点
- 是否提到远端脉搏
- 是否提到皮肤温度/颜色
- 是否提到包扎过紧应松开重缠


## 10. 备注

新增依据: ATP §7-22; 配套 TCCC HEM 卡片

