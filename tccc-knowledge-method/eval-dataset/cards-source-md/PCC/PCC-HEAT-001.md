---
card_id: PCC-HEAT-001
title: PCC 阶段热射病与热衰竭的鉴别与处置
version: '1.0'
module: PCC
topic: PCC 高温伤害
task_type: decision
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
- 成人作战人员
related_cards:
- PCC-PRIN-002
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: HYPERTHERMIA - PCC
  locator: p.24-25
  quote: 'Heat exhaustion: weak, dizzy, nauseated, headache, sweating, normal mental status... Heat stroke: Hyperpyrexia,
    altered mental status... If the casualty is unconscious or vomiting, use IV/IO fluids.'
---

# PCC 阶段热射病与热衰竭的鉴别与处置

## 1. 核心问题

如何在 PCC 环境下区分热衰竭和热射病并分别处置


## 2. 输出目标

让模型输出热衰竭 vs 热射病鉴别 + 现场冷却 + 补液原则


## 3. 适用场景与边界

**适用场景**:
- 热带或沙漠环境的 PCC

**前置条件**:
- 伤员暴露于高温环境

**不覆盖范围**:
- 不覆盖低体温处置 (见 HYP / PCC-HYP)


## 4. 触发与识别

**识别要点**:
- 热衰竭: 虚弱、头晕、恶心、头痛、出汗,意识正常
- 热射病: 高热、无汗或汗液减少,意识改变 (核心区别)


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 热衰竭: 补充水分和电解质 (口服或 IV/IO) | high | 意识正常的高温暴露伤员 | 立即 | 通常可恢复 |
| 2 | 热射病: 立即激进降温 + IV/IO 补液 + 紧急后送 | immediate | 高热 + 意识改变 | 立即 | 热射病是急症,病死率高 |
| 3 | 无意识或呕吐者使用 IV/IO 补液,避免误吸 | immediate | 意识改变或呕吐 | 立即 | Role 1a 起即应执行 |


## 6. 决策点

**1.**
- 如果(condition):意识正常 + 出汗 + 头晕恶心
- 则(next_action):按热衰竭处置
- 依据(rationale):热衰竭可恢复
- 分支类型:`if_then`

**2.**
- 如果(condition):高热 + 意识改变 + 无汗
- 则(next_action):按热射病紧急处置 + 后送
- 依据(rationale):热射病威胁生命
- 分支类型:`escalation`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 把热射病误判为热衰竭延误降温
- 对无意识者口服补液造成误吸


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `HYPERTHERMIA - PCC`
  - 位置: `p.24-25`
  - 原文引用:
    > Heat exhaustion: weak, dizzy, nauseated, headache, sweating, normal mental status... Heat stroke: Hyperpyrexia, altered mental status... If the casualty is unconscious or vomiting, use IV/IO fluids.


## 9. 评分要点(LLM 评测)

- 是否提到意识改变是热射病关键鉴别
- 是否提到立即激进降温
- 是否提到无意识者 IV/IO 补液


## 10. 备注

新增依据: PCC CPG 高温伤害,TCCC 卡片清单未覆盖

