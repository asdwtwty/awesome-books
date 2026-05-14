"""
Evaluation framework content for the knowledge organization method.
"""

EVAL_DIMENSIONS = [
    # (维度, 子指标, 评测方式, 对比基线, 说明)
    ("知识表示有效性", "双格式一致性", "自动化", "N/A",
     "编译前后信息无损率：对比MD源文件语义要素数量与JSONL产物字段数量，计算覆盖率。目标>=99%"),
    ("知识表示有效性", "Schema合规率", "自动化", "N/A",
     "所有卡片通过JSON Schema校验的比例。CI持续检测，目标=100%"),
    ("知识表示有效性", "专家可维护性", "问卷SUS", "直接编辑JSON",
     "邀请3-5名军医使用MD+YAML格式编写卡片，通过SUS量表评估可用性，对比纯JSON编辑"),

    ("检索增强效果", "Recall@K (K=5,10)", "自动化", "固定长度chunk(512token)",
     "给定问题集，比较知识卡片方案与定长切块方案的Top-K召回率"),
    ("检索增强效果", "MRR (Mean Reciprocal Rank)", "自动化", "固定长度chunk",
     "首个正确卡片的排名倒数均值"),
    ("检索增强效果", "语义完整性", "专家评审", "固定长度chunk",
     "返回的知识单元是否语义自足、无需额外上下文即可理解，1-5分人工评分"),

    ("关系扩展效果", "流程覆盖率", "自动化", "无关系扩展",
     "多步流程类问题，关系扩展后覆盖的正确步骤占总步骤比例"),
    ("关系扩展效果", "替代路径命中率", "自动化", "无关系扩展",
     "当首选方案被排除后，系统能否通过alternatives关系找到替代方案"),
    ("关系扩展效果", "关系标注成本", "统计", "知识图谱三元组标注",
     "每张卡片平均标注时间（分钟），与等价知识图谱方案对比"),

    ("安全约束效果", "禁忌违规率", "自动化", "无规则层（纯RAG）",
     "在包含禁忌情境的测试用例中，系统输出违反禁忌证的比例"),
    ("安全约束效果", "规则触发准确率", "半自动", "N/A",
     "规则应触发时正确触发(True Positive) / 不应触发时未误触(True Negative)"),
    ("安全约束效果", "剂量合规率", "自动化", "无规则层",
     "涉及药物剂量的回答中，数值在规则允许范围内的比例"),

    ("端到端生成质量", "Answer Accuracy", "自动化+人工", "纯LLM / 纯向量RAG",
     "基于TCCC考纲题目的选择题准确率 + 开放题专家打分"),
    ("端到端生成质量", "Citation Coverage", "自动化", "纯向量RAG",
     "回答中引用CARD-ID的比例，衡量可溯源程度"),
    ("端到端生成质量", "Hallucination Rate", "人工评审", "纯LLM",
     "回答中包含卡片外自行杜撰内容的比例"),
    ("端到端生成质量", "Response Latency (P95)", "自动化", "纯向量RAG",
     "端到端响应时间95分位值，评估规则层和关系扩展的额外开销"),
]

EVAL_DATASETS = [
    ("事实性问答集", "50题", "来源：TCCC考纲选择题改编",
     "问题类型：单一事实（如'CAT止血带适用部位？'）\n评分：自动匹配标准答案"),
    ("流程性问答集", "30题", "来源：MARCH流程训练大纲",
     "问题类型：多步流程（如'MARCH-H阶段完整处置顺序？'）\n评分：步骤覆盖率+顺序正确率"),
    ("情境决策集", "20题", "来源：专家命题+真实案例改编",
     "问题类型：复杂情境（如'65kg伤员四肢贯穿伤，已用TQ，持续出血，下一步？'）\n评分：专家1-5分"),
    ("禁忌检测集", "25题", "来源：禁忌证规则逆向构造",
     "问题类型：含禁忌触发条件的查询\n评分：禁忌是否被正确拦截/告警"),
    ("替代方案集", "15题", "来源：资源受限场景",
     "问题类型：首选方案不可用时的替代查询\n评分：是否返回有效替代 + 正确性"),
]

ABLATION_EXPERIMENTS = [
    ("Full System", "完整系统（卡片+关系+规则+混合检索）", "基准"),
    ("w/o Relations", "移除关系扩展模块", "评估关系模型贡献"),
    ("w/o Rules", "移除安全规则层", "评估外置规则贡献"),
    ("w/o Card Model", "回退到固定长度chunk（512 token）", "评估卡片模型贡献"),
    ("w/o Hybrid Retrieval", "仅用向量检索，移除BM25", "评估混合检索贡献"),
    ("w/o Structure", "卡片不做结构化分节，纯文本", "评估结构感知贡献"),
]

SAMPLE_CARDS = [
    {
        "id": "CARD-HEM-TQ-001",
        "title": "战术止血带（CAT）四肢大出血控制",
        "module": "MARCH.M",
        "phase": "CUF",
        "task_type": "procedure",
        "summary": "对四肢大出血使用CAT止血带进行紧急止血",
        "steps": [
            "1. 识别四肢活动性大出血（喷射状/涌出/浸透敷料）",
            "2. 取出CAT Gen 7止血带，拉出自由端",
            "3. 将止血带置于出血点近心端5-7cm处（高位放置原则：CUF阶段置于尽可能近心端）",
            "4. 拉紧自由端穿过扣环并回折粘贴",
            "5. 旋转绞棒直至出血停止且远端脉搏消失",
            "6. 将绞棒固定在卡夹中",
            "7. 用记号笔在止血带上标记上带时间",
            "8. 暴露止血带（不得被衣物遮盖）",
        ],
        "contraindications": ["关节部位（膝/肘）", "颈部/躯干"],
        "evidence": "TCCC Guidelines 2024, Section 3.a; CoTCCC Recommendation 2020-01, Grade A"
    },
    {
        "id": "CARD-DRUG-TXA-001",
        "title": "氨甲环酸（TXA）抗纤溶治疗",
        "module": "MARCH.C",
        "phase": "TFC",
        "task_type": "drug",
        "summary": "对预计需要大量输血或合并TBI的伤员给予TXA减少出血",
        "dosage": "2g IV/IO 缓慢推注（10分钟以上）；如无IV/IO通路可IM给药",
        "indication": "预计需要大量输血的创伤伤员；合并显著TBI的伤员",
        "contraindications": ["受伤超过3小时", "已知对TXA过敏"],
        "evidence": "TCCC Guidelines 2024 Proposed Change 20-02; MATTERs Study, Grade A"
    },
    {
        "id": "CARD-AIR-NPA-001",
        "title": "鼻咽通气道（NPA）置入",
        "module": "MARCH.A",
        "phase": "TFC",
        "task_type": "procedure",
        "summary": "对有自主呼吸但意识障碍的伤员建立鼻咽通气道",
        "steps": [
            "1. 评估伤员：有自主呼吸、GCS<=13或打鼾样呼吸",
            "2. 选择合适尺寸NPA（成人通常28F）",
            "3. 润滑NPA外壁",
            "4. 斜面朝向鼻中隔，沿鼻底方向缓慢插入",
            "5. 确认气道通畅（听诊呼吸音、观察胸廓起伏）",
        ],
        "contraindications": ["严重颌面部创伤", "已知颅底骨折"],
        "evidence": "TCCC Guidelines 2024, Airway Management; Grade B"
    },
]

SAMPLE_RULES = [
    {
        "rule_id": "R-HEM-001",
        "name": "关节部位禁用止血带",
        "rule_type": "contraindication",
        "scope": "pre_retrieval",
        "priority": 5,
        "condition_desc": "patient.injury_site IN ['膝关节','肘关节','关节'] → 排除CARD-HEM-TQ-001",
        "action": "exclude_cards: [CARD-HEM-TQ-001]",
        "message": "关节部位不适用止血带，应改用加压包扎或止血填塞",
        "evidence": "TCCC Guidelines 2024, 3.a"
    },
    {
        "rule_id": "R-DRUG-001",
        "name": "TXA时间窗约束",
        "rule_type": "time_constraint",
        "scope": "post_retrieval",
        "priority": 3,
        "condition_desc": "patient.time_since_injury > 3h → 排除CARD-DRUG-TXA-001",
        "action": "exclude_cards + inject_warning",
        "message": "受伤超过3小时，TXA获益不确定且可能增加风险，不推荐使用",
        "evidence": "CRASH-2 Trial; TCCC Proposed Change 20-02"
    },
    {
        "rule_id": "R-DOSE-001",
        "name": "TXA剂量上限校验",
        "rule_type": "dosage_bound",
        "scope": "post_generation",
        "priority": 2,
        "condition_desc": "generated_text中TXA剂量数值 > 2g → 触发告警",
        "action": "inject_warning + rewrite_answer",
        "message": "TXA单次剂量不应超过2g，请核实",
        "evidence": "TCCC Guidelines 2024"
    },
    {
        "rule_id": "R-ESC-001",
        "name": "止血带失效升级",
        "rule_type": "escalation_trigger",
        "scope": "post_retrieval",
        "priority": 8,
        "condition_desc": "patient.tourniquet_applied AND patient.bleeding_continues → 触发升级",
        "action": "include_cards: [CARD-EVAC-URGENT, CARD-HEM-JUNCTIONAL-001]",
        "message": "止血带未能控制出血，应考虑交界区止血器材或紧急后送",
        "evidence": "TCCC Guidelines 2024, 3.c"
    },
]

SAMPLE_RELATIONS = [
    ("REL-0001", "CARD-HEM-TQ-001", "precedes", "CARD-HEM-WOUND-002",
     "止血带控制出血后进行伤口包扎"),
    ("REL-0002", "CARD-HEM-TQ-001", "alternatives", "CARD-HEM-PRESSURE-003",
     "直接加压可作为止血带的替代（非大出血时）"),
    ("REL-0003", "CARD-HEM-TQ-001", "forbids_with", "CARD-HEM-JOINT-TQ",
     "标准CAT与关节部位止血不兼容"),
    ("REL-0004", "CARD-HEM-TQ-001", "escalates_to", "CARD-EVAC-URGENT",
     "止血带无效时升级到紧急后送"),
    ("REL-0005", "CARD-MARCH-H-OVERVIEW", "refines", "CARD-HEM-TQ-001",
     "MARCH-H总览细化到具体止血带操作"),
    ("REL-0006", "CARD-AIR-NPA-001", "precedes", "CARD-AIR-RECOVERY-001",
     "NPA置入后摆放恢复体位"),
    ("REL-0007", "CARD-AIR-NPA-001", "alternatives", "CARD-AIR-CRIC-001",
     "当NPA无法建立通气道时考虑环甲膜切开"),
    ("REL-0008", "CARD-AIR-NPA-001", "escalates_to", "CARD-AIR-CRIC-001",
     "NPA失败则升级到外科气道"),
    ("REL-0009", "CARD-DRUG-TXA-001", "triggered_by", "COND-MAJOR-HEMORRHAGE",
     "大出血条件触发TXA给药"),
    ("REL-0010", "CARD-DRUG-TXA-001", "precedes", "CARD-FLUID-RESUS-001",
     "TXA给药先于液体复苏"),
]
