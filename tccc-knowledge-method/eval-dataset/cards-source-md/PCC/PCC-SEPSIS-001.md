---
card_id: PCC-SEPSIS-001
title: PCC 阶段脓毒症识别与三档抗感染方案
version: '1.0'
module: PCC
topic: PCC 抗生素与脓毒症
task_type: decision
training_use:
- fact_qa
- case_qa
- structured_decision
- retrieval
difficulty: advanced
applicable_phase:
- prolonged_casualty_care
evidence_level: guideline
review_status: draft
reviewers: []
created_at: '2026-05-16'
updated_at: '2026-05-16'
applicable_population:
- 开放性创伤伤员
related_cards:
- ABX-002
- ABX-003
source_refs:
- source_id: JTS-PCC-CPG-91
  title: Prolonged Casualty Care Guidelines
  version: CPG ID:91
  section: ANTIBIOTICS, SEPSIS, AND OTHER DRUGS - PCC
  locator: p.40 Table 14
  quote: Minimum - Moxifloxacin 400 mg PO daily; Better - Ertapenem 1 gram IV/IO every 24 hours OR ceftriaxone 2 grams IV/IO
    every 24 hrs; Best - ceftriaxone 2 grams IV/IO every 24 hrs., PLUS vancomycin 1.5 mg/kg IV/IO every 12 hours, PLUS metronidazole
    500 mg IV/PO/IO every 8 hours.
---

# PCC 阶段脓毒症识别与三档抗感染方案

## 1. 核心问题

PCC 阶段的脓毒症如何识别并按 minimum/better/best 选择抗生素


## 2. 输出目标

让模型输出脓毒症 PCC 三档治疗方案 + 早期识别要点


## 3. 适用场景与边界

**适用场景**:
- PCC > 12 小时的伤员
- 未及时清创或包扎

**前置条件**:
- TCCC 抗生素首剂已给

**不覆盖范围**:
- 不覆盖确定性外科清创


## 4. 触发与识别

**触发条件**:
- 钝伤或穿透伤后未及时治疗
- 新发发热、心率上升、低血压

**识别要点**:
- 意识改变或精神状态变化
- 心率持续升高
- 低血压
- 发热或低体温


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | Minimum: 莫西沙星 400 mg PO 每日 | high | 可口服 + 资源最少 | 立即 | TCCC 一线已用药者继续 |
| 2 | Better: 厄他培南 1 g IV/IO 每 24 小时,或头孢曲松 2 g IV/IO 每 24 小时 | high | 无法口服或更高资源 | 立即 | 覆盖革兰阴性 + 厌氧 |
| 3 | Best: 头孢曲松 2 g IV/IO Q24h + 万古霉素 1.5 mg/kg IV/IO Q12h + 甲硝唑 500 mg Q8h | high | Role 1c + 严重脓毒症 | 立即 | 三联广覆盖,需考虑过敏与肾功能 |


## 6. 决策点

**1.**
- 如果(condition):确认或高度怀疑脓毒症
- 则(next_action):按当前可用资源选择 minimum/better/best 之一
- 依据(rationale):PCC 资源决定方案选择
- 分支类型:`if_then`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 等待发热出现才考虑脓毒症
- 只用 TCCC 首剂不升级


## 8. 证据来源(展开)

- **JTS-PCC-CPG-91** — Prolonged Casualty Care Guidelines (CPG ID:91)
  - 章节: `ANTIBIOTICS, SEPSIS, AND OTHER DRUGS - PCC`
  - 位置: `p.40 Table 14`
  - 原文引用:
    > Minimum - Moxifloxacin 400 mg PO daily; Better - Ertapenem 1 gram IV/IO every 24 hours OR ceftriaxone 2 grams IV/IO every 24 hrs; Best - ceftriaxone 2 grams IV/IO every 24 hrs., PLUS vancomycin 1.5 mg/kg IV/IO every 12 hours, PLUS metronidazole 500 mg IV/PO/IO every 8 hours.


## 9. 评分要点(LLM 评测)

- 是否提到三档方案 (minimum/better/best)
- 是否提到莫西沙星 / 厄他培南 / 头孢曲松剂量
- 是否提到早期识别征象


## 10. 备注

新增依据: PCC CPG; TCCC ABX 卡片不覆盖脓毒症升级

