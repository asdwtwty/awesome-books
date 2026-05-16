---
card_id: ATP-CHOKE-001
title: 气道梗阻识别与海姆立克手法 (含特殊体型替代手法)
version: '1.0'
module: ATP
topic: 气道
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
- 成人意识清醒伤员
related_cards:
- AIR-002
- AIR-006
source_refs:
- source_id: ATP-4-02.11
  title: Army Techniques Publication for Casualty Response, TCCC, and First Aid
  version: March 2026
  section: Chapter 5 Airway Control
  locator: 5-31, p.67
  quote: Use abdominal thrusts, also known as the Heimlich maneuver... For individuals in advanced stages of pregnancy, those
    who are markedly obese, or if there is a significant abdominal wound, use chest thrust instead.
---

# 气道梗阻识别与海姆立克手法 (含特殊体型替代手法)

## 1. 核心问题

ATP 4-02.11 推荐何种手法清除上气道完全梗阻


## 2. 输出目标

让模型输出腹部冲击 + 胸部冲击的适应证差异


## 3. 适用场景与边界

**适用场景**:
- 陆军非战术急救
- TFC 阶段非穿透性气道梗阻

**前置条件**:
- 伤员意识清醒但发声/咳嗽弱或不能呼吸

**不覆盖范围**:
- 不覆盖创伤性气道梗阻 (见 AIR 模块)


## 4. 触发与识别

**识别要点**:
- 高音呼吸声或咳嗽声 (gas exchange 不足)
- 无法呼吸
- 通用窒息手势 (双手抓喉)


## 5. 关键动作 / 流程

| 步骤 | 动作 | 优先级 | 条件 | 时间目标 | 备注 |
|---|---|---|---|---|---|
| 1 | 默认: 使用腹部冲击 (海姆立克),双手放腰部与肋骨之间,快速向上推顶 | immediate | 意识清醒成人 + 完全气道梗阻 | 立即 | 首选标准技术 |
| 2 | 替代: 对孕晚期、明显肥胖或腹部有大伤口者改用胸部冲击 | immediate | 腹部冲击不可行 | 立即 | 双手放胸骨中部,锐利向内向上推 |
| 3 | 立即呼救并准备升级处置 | high | 梗阻持续 | 立即 | 防止意识丧失 |


## 6. 决策点

**1.**
- 如果(condition):孕晚期/重度肥胖/腹部伤
- 则(next_action):用胸部冲击代替腹部冲击
- 依据(rationale):腹部冲击会加重原有伤情
- 分支类型:`if_else`


## 7. 复评 / 终点 / 禁忌 / 错误

**常见错误**:
- 对孕妇用腹部冲击
- 动作太轻无效


## 8. 证据来源(展开)

- **ATP-4-02.11** — Army Techniques Publication for Casualty Response, TCCC, and First Aid (March 2026)
  - 章节: `Chapter 5 Airway Control`
  - 位置: `5-31, p.67`
  - 原文引用:
    > Use abdominal thrusts, also known as the Heimlich maneuver... For individuals in advanced stages of pregnancy, those who are markedly obese, or if there is a significant abdominal wound, use chest thrust instead.


## 9. 评分要点(LLM 评测)

- 是否提到默认腹部冲击
- 是否提到孕晚期/肥胖/腹伤改胸部冲击
- 是否提到通用窒息手势识别


## 10. 备注

新增依据: ATP §5-31; TCCC AIR 模块未明确海姆立克替代方案

