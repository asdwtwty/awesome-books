---
card_id: ATP-CCP-001
title: 伤员收容点 (CCP) 选址与建立标准
version: '1.0'
module: ATP
topic: 伤员收容点
task_type: procedure
training_use:
- fact_qa
- case_qa
- retrieval
difficulty: intermediate
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
- TRIAGE-001
- EVAC-001
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 1 Casualty Collection Point Site Selection
  locator: 1-28, p.7
  quote: 'The CCP should be established with: A day and night marking system; A triage point for entry into and exit from
    the CCP; Properly marked evacuation categories; A killed in action (KIA) area away from the other casualties; A medical
    resupply area; A helicopter landing zone (HLZ).'
---

# 伤员收容点 (CCP) 选址与建立标准

## 1. 核心问题

如何选址和建立伤员收容点 (Casualty Collection Point, CCP)


## 2. 输出目标

让模型输出 CCP 必备的 6 项要素 + 选址原则


## 3. 适用场景与边界

**适用场景**:
- 排连级战场
- 野外战术行动

**前置条件**:
- 排级以上单位在战场行动中

**不覆盖范围**:
- 不覆盖具体救治流程
- 不覆盖航空后送


## 4. 触发与识别

_(暂无)_


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 在排级单位 SOP 中预先规划 CCP 选址并演练 | high | 战术行动前 | 事前 | 由首席士官或排长决定 |
| 2 | CCP 必备 6 项: 昼夜标识系统 / 入出口分诊点 / 撤运分类标识 / KIA 区 / 医疗补给区 / HLZ | high | 建立 CCP | 立即 | ATP 1-28 项 6 个最低要素 |
| 3 | 用墙体或隔断按分诊类别分区,房间按颜色编码 | high | 建在建筑物内 | 立即 | 提高监护可视性 |


## 6. 决策点

**1.**
- 如果(condition):建在开阔地
- 则(next_action):用刚性或杆式担架便于移动
- 依据(rationale):开阔地暴露大
- 分支类型:`if_then`

**2.**
- 如果(condition):建在建筑物内
- 则(next_action):用最大房间,按治疗分类分别用不同房间
- 依据(rationale):降低监护盲区
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 无 KIA 专门区致混淆
- 无 HLZ 难以快速后送
- 夜间无标识致 CCP 难定位


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 1 Casualty Collection Point Site Selection`
  - 位置: `1-28, p.7`
  - 原文引用:
    > The CCP should be established with: A day and night marking system; A triage point for entry into and exit from the CCP; Properly marked evacuation categories; A killed in action (KIA) area away from the other casualties; A medical resupply area; A helicopter landing zone (HLZ).


## 9. 评分要点(LLM 评测)

- 是否提到 6 项必备要素
- 是否提到昼夜标识系统
- 是否提到 HLZ 必备
- 是否提到 KIA 单独区


## 10. 备注

新增依据: ATP 4-02.11; TCCC 卡片清单未覆盖 CCP 建立

