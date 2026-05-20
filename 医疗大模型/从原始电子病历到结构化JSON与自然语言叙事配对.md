# 从原始电子病历到"结构化 JSON + 自然语言叙事配对"

> 本文档整理了构建创伤大语言模型 MVP 第 1 步——专病数据库训练语料加工的完整方法论。
> 适用于基于专病数据库（如创伤、卒中、肿瘤等）构建领域大模型的训练数据准备阶段。

---

## 引言

构建创伤大语言模型 MVP 的第 1 步（1-2 个月）：先把专病数据库的 1000 例典型病例转成结构化 JSON + 自然语言叙事配对。

这一步的本质是：**把医院 HIS/EMR 系统里散落、异构、口语化的原始数据，加工成大模型能"吃"的高质量训练样本**。本文从四个层次讲清楚整个流程。

---

## 一、什么是"结构化 JSON + 自然语言叙事配对"？

### 1.1 核心思想

每一例病例最终产出一对配套的数据：

```
┌─────────────────────────┐    ┌─────────────────────────┐
│   结构化 JSON           │    │   自然语言叙事           │
│   (机器友好)             │ ⇄  │   (语言模型友好)         │
│   - 字段清晰             │    │   - 流畅连贯             │
│   - 编码标准化            │    │   - 临床语境完整         │
│   - 可查询统计            │    │   - 接近真实病历          │
└─────────────────────────┘    └─────────────────────────┘
         同一病例的两种表示，通过 case_id 绑定
```

### 1.2 一个具体例子

**原始 EMR 片段（脏数据）**：

```
入院记录
姓名：张某某  性别：男  年龄：45岁  身份证：3201**********1234
主诉：车祸致全身多处疼痛2小时
现病史：患者2小时前骑电动车被一小轿车从右侧撞击，当即倒地，
意识模糊约5分钟，120送来。查：BP 85/50, P 120, R 28, SpO2 92%,
GCS E2V3M4=9。胸片示右侧多发肋骨骨折，腹部FAST(+)。
急诊行剖腹探查+脾切除术...
```

**加工后 → 结构化 JSON**：

```json
{
  "case_id": "TR-2024-001",
  "demographics": {
    "age": 45,
    "sex": "male"
  },
  "injury_event": {
    "mechanism": "MVC",
    "mechanism_detail": "电动车被小轿车右侧撞击",
    "time_to_hospital_min": 120,
    "loc_duration_min": 5
  },
  "vital_signs_on_arrival": {
    "sbp": 85, "dbp": 50,
    "hr": 120, "rr": 28, "spo2": 92,
    "gcs": {"e": 2, "v": 3, "m": 4, "total": 9}
  },
  "injuries": [
    {"region": "chest", "type": "rib_fracture", "side": "right", "ais": 3},
    {"region": "abdomen", "organ": "spleen", "ais": 4}
  ],
  "scores": {"iss": 25, "rts": 5.97, "trauma_triage": "red"},
  "interventions": [
    {"type": "surgery", "name": "exploratory_laparotomy", "time_min": 45},
    {"type": "surgery", "name": "splenectomy", "time_min": 45}
  ],
  "outcome": {"survival": true, "icu_days": 7, "hospital_days": 21}
}
```

**加工后 → 自然语言叙事**：

```
患者男性，45岁，因"车祸致全身多处疼痛2小时"入院。

【损伤机制】患者2小时前驾驶电动车时被小轿车从右侧撞击，
当即倒地，伤后意识模糊约5分钟。

【入院评估】生命体征：血压85/50 mmHg，心率120次/分，
呼吸28次/分，血氧饱和度92%；GCS 评分9分（E2V3M4），
意识中度障碍。患者表现为失代偿性休克。

【损伤诊断】(1) 右侧多发肋骨骨折（AIS 3）；(2) 脾破裂（AIS 4）。
ISS 评分 25 分，属重度多发伤；RTS 评分 5.97；创伤分检为红色（危重）。

【处置】立即启动大量输血方案，在伤后约45分钟行剖腹探查+脾切除术。

【转归】术后入ICU监护7天，住院21天后好转出院。
```

---

## 二、对原始电子病历需要做的具体处理

整个加工流程分 **6 个步骤**。

### 步骤 1：数据采集与隐私脱敏（最先做）

#### 采集来源（典型创伤病例涉及）

- **HIS**：基本信息、费用
- **EMR**：入院记录、病程记录、手术记录、出院小结
- **LIS**：检验结果（血气、血常规、凝血等）
- **RIS/PACS**：影像报告
- **急诊系统**：120 院前记录、急诊抢救记录
- **麻醉系统**：术中生命体征
- **ICU 系统**：监护数据

#### 脱敏要点（GB/T 35273-2020 + HIPAA 18 项）

| 必须移除 | 处理方式 |
|---------|---------|
| 姓名 | 替换为 "患者A" 或哈希 ID |
| 身份证、电话 | 删除 |
| 详细住址 | 模糊到市/区级 |
| 床号、住院号 | 用 case_id 替代 |
| 主管医生姓名 | 替换为角色（"主刀医生"） |
| 入院日期 | 偏移随机天数（保留时间间隔） |

> **注意**：年龄、性别、伤情数据**必须保留**，这些是临床有效信息。

---

### 步骤 2：术语标准化与编码映射

原始病历充斥着同义词、缩写、口语表达，必须统一：

| 原始表达 | 标准化结果 |
|---------|----------|
| "脾破"、"脾脏挫裂伤"、"脾损伤III级" | `spleen_injury_AAST_grade_3` |
| "失血性休克"、"低血容量休克" | `hemorrhagic_shock` |
| "BP 85/50"、"血压偏低 85/50" | `sbp: 85, dbp: 50` |
| "120送来"、"急救车送入" | `transport: EMS` |

#### 推荐使用的编码体系

- **诊断**：ICD-10/11
- **损伤严重度**：AIS 2015 / ISS
- **手术**：ICD-9-CM-3 或 ICHI
- **药物**：ATC 或 RxNorm
- **检验**：LOINC
- **总体术语**：SNOMED CT（如条件允许）

---

### 步骤 3：信息抽取（NLP / 人工 / 混合）

这是**最核心也最耗时**的环节。三种实现方式：

#### 方式 A：纯人工标注（金标准，但慢）

医生 + 标注员按 schema 逐条填写。1000 例约需 3-5 个标注员 × 1 个月。

#### 方式 B：LLM 辅助抽取 + 人工审核（推荐）

```
原始病历文本
    ↓ Prompt 工程（给定 JSON schema）
GPT-4 / Claude / DeepSeek 自动抽取
    ↓
医生快速审核修正（每例 5-10 分钟）
    ↓
入库
```

效率可提升 5-10 倍，质量可控。

#### 方式 C：规则 + 微调小模型（适合大规模）

- 正则提取生命体征、化验值（结构相对固定）
- BERT/UIE 微调模型抽取实体关系
- 适合后期上规模时使用

---

### 步骤 4：定义 JSON Schema（必须先做！）

**这是最容易被忽略但最关键的一步**。建议按创伤救治时间轴设计：

```yaml
trauma_case_schema:
  case_id              # 唯一标识
  demographics         # 人口学
  pre_hospital         # 院前数据
    - mechanism        # 损伤机制（MVC/坠落/锐器/钝器/烧伤...）
    - scene_vitals     # 现场生命体征
    - first_aid        # 院前处置
  ed_arrival           # 急诊入院
    - vitals           # 生命体征
    - gcs              # 意识评分
    - primary_survey   # ABCDE 评估结果
    - secondary_survey # 全身详查
  diagnostics          # 检查结果
    - imaging          # CT/X线/B超/FAST
    - labs             # 检验
  injuries[]           # 损伤清单（数组）
    - region
    - organ
    - ais_code
    - ais_severity
  scores               # 评分汇总
    - iss, rts, trauma_score, gcs_total
  interventions[]      # 治疗干预
    - type             # 输血/手术/介入/药物
    - name
    - time_from_injury_min
  course               # 病程
    - icu_events
    - complications
  outcome              # 转归
    - survival
    - los_days
    - discharge_status
```

#### 建议参考国际标准

- 美国 NTDB（National Trauma Data Bank）数据字典
- 中国 CHTR（中国创伤数据库）字段
- TQIP（Trauma Quality Improvement Program）规范

---

### 步骤 5：自然语言叙事生成

从结构化 JSON 反向生成流畅病历叙事，有三种策略：

#### 策略 1：模板填充（快、稳定、但单调）

```python
template = "患者{sex}性，{age}岁，因{chief_complaint}入院。"
           "入院时血压{sbp}/{dbp} mmHg，GCS {gcs_total}分。"
           "诊断：{injuries_text}。ISS评分{iss}分。"
```

#### 策略 2：LLM 改写（多样、自然、推荐）

把 JSON 喂给 GPT-4，让它"扮演主治医生写一份首程记录"，可生成多种风格变体（数据增强）。

#### 策略 3：保留原始病历叙事 + 对齐

直接用脱敏后的原文作为叙事，与抽取的 JSON 配对。**真实性最高**，但需要做好脱敏。

> **推荐组合**：策略 3 为主（真实性）+ 策略 2 补充多样性。

---

### 步骤 6：质量控制与版本管理

#### 质控指标

- 字段完整率（必填字段缺失率 < 5%）
- 编码一致性（双人标注 Kappa > 0.85）
- 临床合理性（医生抽查 10%）
- 叙事-JSON 一致性（关键字段双向校验）

#### 版本管理

- 用 Git/DVC 管理数据集版本
- 标注每条数据的来源、标注人、标注时间、审核状态
- 建立异常病例回溯机制

---

## 三、最终训练样本的形态（这才是大模型实际看到的）

加工完后，1 个病例可以衍生出多种训练样本：

### 样本类型 1：病例摘要任务

```json
{
  "instruction": "请根据以下结构化病历数据生成一份首次病程记录",
  "input": "<结构化JSON>",
  "output": "<自然语言叙事>"
}
```

### 样本类型 2：信息抽取任务（反向）

```json
{
  "instruction": "请从以下病历中抽取损伤部位、AIS评分和ISS评分",
  "input": "<自然语言病历>",
  "output": "<结构化JSON>"
}
```

### 样本类型 3：临床决策问答

```json
{
  "instruction": "患者男45岁，车祸伤，BP 85/50，FAST(+)，下一步处置？",
  "input": "",
  "output": "提示腹腔内出血+失血性休克。立即：①建立两路大孔径静脉..."
}
```

### 样本类型 4：评分推理

```json
{
  "instruction": "根据损伤情况计算ISS评分",
  "input": "右侧多发肋骨骨折(AIS 3)；脾破裂(AIS 4)",
  "output": "ISS = 3² + 4² = 9 + 16 = 25分"
}
```

> **1 个高质量病例 → 5-10 个训练样本**，1000 例可产出 5000-10000 条 SFT 数据，足够做出有效的 LoRA 微调。

---

## 四、推荐的工具链

| 环节 | 推荐工具 |
|------|---------|
| 数据脱敏 | Microsoft Presidio（英文）/ 自研规则+NER（中文） |
| 标注平台 | Label Studio / doccano / Prodigy |
| 术语映射 | UMLS（英）/ 国家临床医学术语库（中） |
| LLM 抽取 | GPT-4o、Claude、DeepSeek-V3、Qwen-Max |
| Schema 校验 | JSON Schema、Pydantic |
| 数据版本 | DVC、HuggingFace Datasets |
| 质控统计 | Pandas + Great Expectations |

---

## 五、落地建议

如果你是项目负责人，按以下顺序推进：

| 时间 | 任务 |
|------|------|
| 第 1 周 | 组建 3-5 人小组（1 位高年资创伤外科医生 + 1 位住院医生 + 1 位 NLP 工程师 + 1 位数据工程师 + 1 位 PM） |
| 第 2 周 | 定 schema，先用 10 例做端到端跑通，调整 schema |
| 第 3-4 周 | 扩到 100 例，建立标注规范文档（SOP） |
| 第 5-8 周 | 扩到 1000 例，并行做质控 |
| 第 8 周末 | 交付 1000 例配对数据 + 数据字典 + 标注 SOP |

---

## 六、关键检查清单（Checklist）

在交付前请逐项确认：

- [ ] 所有 PHI 已脱敏，通过隐私扫描工具复检
- [ ] JSON Schema 已固化为机器可校验文件（JSON Schema / Pydantic）
- [ ] 每例数据包含完整的 metadata（来源、标注人、时间、版本）
- [ ] 双人标注一致性（Kappa）≥ 0.85
- [ ] 至少 10% 的样本由资深创伤外科医生终审
- [ ] 自然语言叙事与 JSON 关键字段双向可还原
- [ ] 数据集已纳入 Git/DVC 版本管理
- [ ] 已建立异常病例回溯与修正机制
- [ ] 已签署数据使用合规协议（伦理委员会批件）

---

## 附录 A：术语对照速查表

| 中文 | 英文缩写 | 全称 |
|------|---------|------|
| 简明损伤定级 | AIS | Abbreviated Injury Scale |
| 损伤严重度评分 | ISS | Injury Severity Score |
| 修正创伤评分 | RTS | Revised Trauma Score |
| 创伤损伤严重度评分法 | TRISS | Trauma and Injury Severity Score |
| 格拉斯哥昏迷评分 | GCS | Glasgow Coma Scale |
| 重点超声创伤评估 | FAST | Focused Assessment with Sonography for Trauma |
| 损伤控制性手术 | DCS | Damage Control Surgery |
| 损伤控制性复苏 | DCR | Damage Control Resuscitation |
| 大量输血方案 | MTP | Massive Transfusion Protocol |
| 美国国家创伤数据库 | NTDB | National Trauma Data Bank |
| 中国创伤数据库 | CHTR | Chinese Trauma Database |

---

## 附录 B：参考资源

- **NTDB Data Dictionary**：美国创伤外科学会发布的标准字段定义
- **AIS 2015**：损伤严重度编码标准
- **AAST Organ Injury Scale**：器官损伤分级
- **ATLS（高级创伤生命支持）指南**：第 10 版
- **《中国创伤救治规范》**：中华医学会创伤学分会
- **HIPAA Safe Harbor**：18 项 PHI 标识符清单
- **GB/T 35273-2020**：信息安全技术 个人信息安全规范

---

*本文档为创伤大语言模型 MVP 项目的方法论指南，可直接作为团队 SOP 的基础材料使用。*
