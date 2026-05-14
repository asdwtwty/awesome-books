#!/usr/bin/env python3
"""
Generate Word document: 战创伤救护知识组织与表示方法 - Schema设计与评估框架
"""
import sys
sys.path.insert(0, '/projects/sandbox/awesome-books')

from docx_helper import DocxWriter
from content_schemas import (
    CARD_SCHEMA_JSON, RULE_SCHEMA_JSON, RELATION_SCHEMA_JSON,
    RELATION_TYPE_DEFINITIONS, 
)
from content_evaluation import (
    EVAL_DIMENSIONS, EVAL_DATASETS, ABLATION_EXPERIMENTS,
    SAMPLE_CARDS, SAMPLE_RULES, SAMPLE_RELATIONS,
)

def main():
    doc = DocxWriter()
    
    # ===== 封面 =====
    doc.add_empty_line()
    doc.add_empty_line()
    doc.add_heading("面向大模型调用的战创伤救护知识组织与表示方法", 1)
    doc.add_heading("原型系统Schema设计与应用研究评估框架", 2)
    doc.add_empty_line()
    doc.add_paragraph("基于TCCC（战术战伤救治）与PFC（延续野战救护）文档")
    doc.add_paragraph("文档版本：1.0.0")
    doc.add_paragraph("日期：2026年5月")
    doc.add_empty_line()
    doc.add_empty_line()

    # ===== 目录 =====
    doc.add_heading("目  录", 1)
    toc_items = [
        "第一章  应用研究评估视角与方法论",
        "  1.1 评估维度与指标体系",
        "  1.2 评测数据集设计",
        "  1.3 消融实验方案",
        "  1.4 评估流程",
        "第二章  知识卡片模型Schema",
        "  2.1 设计原则",
        "  2.2 完整JSON Schema定义",
        "  2.3 字段说明表",
        "  2.4 示例卡片",
        "第三章  安全规则层Schema",
        "  3.1 设计原则",
        "  3.2 完整JSON Schema定义",
        "  3.3 规则类型与执行阶段",
        "  3.4 示例规则",
        "第四章  轻量关系模型Schema",
        "  4.1 六类关系定义",
        "  4.2 完整JSON Schema定义",
        "  4.3 关系驱动的检索扩展策略",
        "  4.4 示例关系",
        "第五章  一体化调用框架设计",
        "  5.1 系统架构",
        "  5.2 调用管线流程",
        "  5.3 Prompt模板设计",
    ]
    for item in toc_items:
        doc.add_paragraph(item)
    doc.add_empty_line()

    # ============================================================
    # 第一章：评估框架
    # ============================================================
    doc.add_heading("第一章  应用研究评估视角与方法论", 1)
    
    doc.add_paragraph(
        "从应用研究角度评估本知识组织方法，核心问题是：相比现有方案（纯向量RAG、"
        "固定长度切块、无规则层），本方法在战创伤救护这一安全敏感领域中，"
        "能否在检索精度、安全约束、可维护性和端到端生成质量四个方面带来可量化的提升。"
    )
    doc.add_paragraph(
        "本章提出一套四维评估体系，涵盖16项具体指标，配合5类评测数据集和6组消融实验，"
        "为原型系统的有效性验证提供完整的方法论支撑。"
    )
    
    doc.add_heading("1.1 评估维度与指标体系", 2)
    doc.add_paragraph(
        "评估分为四个维度：知识表示有效性、检索增强效果、安全约束效果、端到端生成质量。"
        "每个维度下设若干子指标，指定评测方式和对比基线。"
    )
    
    headers = ["维度", "子指标", "评测方式", "对比基线", "说明"]
    rows = [(d[0], d[1], d[2], d[3], d[4]) for d in EVAL_DIMENSIONS]
    doc.add_table(headers, rows)
    
    doc.add_heading("1.2 评测数据集设计", 2)
    doc.add_paragraph("为保证评估可复现、规模可控，设计以下5类评测集：")
    headers = ["数据集", "规模", "来源", "说明"]
    rows = [(d[0], d[1], d[2], d[3]) for d in EVAL_DATASETS]
    doc.add_table(headers, rows)
    
    doc.add_heading("1.3 消融实验方案", 2)
    doc.add_paragraph(
        "通过逐一移除系统组件，量化各模块的独立贡献。共6组实验："
    )
    headers = ["实验组", "配置说明", "目的"]
    rows = [(d[0], d[1], d[2]) for d in ABLATION_EXPERIMENTS]
    doc.add_table(headers, rows)
    
    doc.add_heading("1.4 评估流程", 2)
    doc.add_paragraph("评估按以下四阶段执行：", bold=True)
    steps = [
        "阶段一 - 知识库构建与校验（2周）：完成MARCH全模块约80张卡片编写、关系标注、规则编写，通过CI全量Schema校验。",
        "阶段二 - 检索层评测（1周）：使用事实性+流程性问答集，对比Full System与w/o Card Model、w/o Hybrid Retrieval的Recall@K和MRR。",
        "阶段三 - 安全层评测（1周）：使用禁忌检测集，对比Full System与w/o Rules的禁忌违规率和规则触发准确率。",
        "阶段四 - 端到端评测（1周）：使用全部5类数据集，对比Full System与所有消融组的Answer Accuracy、Citation Coverage和Hallucination Rate。",
    ]
    for s in steps:
        doc.add_bullet(s)
    doc.add_empty_line()
    
    doc.add_paragraph("统计方法：", bold=True)
    stat_items = [
        "自动化指标：报告均值±标准差，使用配对t检验（p<0.05）判断显著性",
        "人工评分：3名评审者独立打分，报告Fleiss Kappa一致性系数",
        "效率指标：统计P50/P95延迟，对比规则层开启/关闭的额外开销",
    ]
    for s in stat_items:
        doc.add_bullet(s)
    doc.add_empty_line()

    # ============================================================
    # 第二章：知识卡片Schema
    # ============================================================
    doc.add_heading("第二章  知识卡片模型Schema", 1)
    
    doc.add_heading("2.1 设计原则", 2)
    principles = [
        "一卡一动作/一概念：每张卡片对应TCCC/PFC中一个可独立问答的最小知识单元",
        "语义自足：卡片脱离上下文仍可理解，body.summary字段必填",
        "可独立验证：每卡至少一条evidence来源，支持溯源审计",
        "双表示统一：YAML frontmatter为人工维护态，JSON为机器调用态，编译器保证一致性",
        "类型区分：5种task_type对应不同必填字段，Schema层面强制约束",
    ]
    for p in principles:
        doc.add_bullet(p)
    doc.add_empty_line()
    
    doc.add_heading("2.2 完整JSON Schema定义", 2)
    doc.add_paragraph("以下为知识卡片的JSON Schema（draft-07标准）：")
    doc.add_code_block(CARD_SCHEMA_JSON.split('\n'))
    doc.add_empty_line()
    
    doc.add_heading("2.3 字段说明表", 2)
    card_fields = [
        ("id", "string", "是", "全局唯一标识，格式CARD-{模块}-{简写}-{序号}"),
        ("title", "string", "是", "卡片标题，<=80字符"),
        ("version", "string", "是", "语义版本号 major.minor.patch"),
        ("updated", "date", "是", "最后更新日期"),
        ("authors", "array[string]", "否", "编写/审核人员"),
        ("module", "enum", "是", "所属MARCH/PAWS/PFC模块"),
        ("phase", "enum", "是", "适用救治阶段CUF/TFC/TACEVAC/PFC"),
        ("task_type", "enum", "是", "卡片类型：procedure/decision/knowledge/drug/equipment"),
        ("applicable_to", "array[string]", "否", "适应证标签"),
        ("contraindications", "array[string]", "否", "禁忌证标签"),
        ("patient_group", "array[enum]", "否", "适用人群"),
        ("body.summary", "string", "是", "一句话摘要"),
        ("body.steps", "array[string]", "procedure必填", "操作步骤"),
        ("body.criteria", "array[string]", "decision必填", "判断标准"),
        ("body.dosage", "object", "drug必填", "剂量/途径/频次/上限"),
        ("body.notes", "array[string]", "否", "注意事项"),
        ("evidence", "array[object]", "是", "至少一条证据来源+等级"),
        ("tags", "array[string]", "否", "检索标签/同义词"),
        ("related", "object", "否", "六类关系引用"),
        ("hash", "string", "自动生成", "内容SHA-256防篡改"),
    ]
    doc.add_table(
        ["字段", "类型", "必填", "说明"],
        card_fields
    )
    
    doc.add_heading("2.4 示例卡片", 2)
    for card in SAMPLE_CARDS:
        doc.add_paragraph(f"【{card['id']}】{card['title']}", bold=True)
        doc.add_bullet(f"模块: {card['module']}  |  阶段: {card['phase']}  |  类型: {card['task_type']}")
        doc.add_bullet(f"摘要: {card['summary']}")
        if 'steps' in card:
            doc.add_paragraph("操作步骤：")
            for step in card['steps']:
                doc.add_bullet(step)
        if 'dosage' in card:
            doc.add_bullet(f"用药方案: {card['dosage']}")
        if 'indication' in card:
            doc.add_bullet(f"适应证: {card['indication']}")
        doc.add_bullet(f"禁忌证: {', '.join(card['contraindications'])}")
        doc.add_bullet(f"证据: {card['evidence']}")
        doc.add_empty_line()

    # ============================================================
    # 第三章：安全规则层Schema
    # ============================================================
    doc.add_heading("第三章  安全规则层Schema", 1)
    
    doc.add_heading("3.1 设计原则", 2)
    rule_principles = [
        "外置化：安全约束独立于知识正文存储和执行，不依赖LLM理解自然语言中的禁忌",
        "多阶段执行：规则可在检索前（硬过滤）、检索后（重排/冲突检测）、生成后（校验/改写）三阶段分别触发",
        "声明式条件：使用JSON-Logic语法表达条件，可被程序自动求值，无需自然语言解析",
        "优先级仲裁：冲突规则按priority字段排序，高优先级覆盖低优先级",
        "证据溯源：每条规则必须标注依据来源，支持审计追踪",
        "可开关：enabled字段支持灰度发布和AB测试",
    ]
    for p in rule_principles:
        doc.add_bullet(p)
    doc.add_empty_line()
    
    doc.add_heading("3.2 完整JSON Schema定义", 2)
    doc.add_paragraph("以下为安全规则的JSON Schema：")
    doc.add_code_block(RULE_SCHEMA_JSON.split('\n'))
    doc.add_empty_line()
    
    doc.add_heading("3.3 规则类型与执行阶段", 2)
    doc.add_paragraph("系统支持6种规则类型，每种对应特定的触发场景：")
    rule_types = [
        ("contraindication", "禁忌证", "pre_retrieval", "根据伤员状态排除不适用的知识卡片"),
        ("priority_override", "优先级覆盖", "post_retrieval", "根据伤情紧急程度调整卡片排序"),
        ("escalation_trigger", "升级触发", "post_retrieval", "当前处置无效时自动引入升级方案"),
        ("dosage_bound", "剂量边界", "post_generation", "校验LLM输出的药物剂量是否在允许范围"),
        ("time_constraint", "时间约束", "post_retrieval", "超出时间窗的处置予以排除"),
        ("combination_forbidden", "联合禁忌", "post_retrieval", "检测多卡片间的禁忌组合"),
    ]
    doc.add_table(
        ["类型标识", "中文名", "典型执行阶段", "功能说明"],
        rule_types
    )
    
    doc.add_paragraph("三阶段执行时序：", bold=True)
    stage_items = [
        "Pre-retrieval（检索前）：在向量/BM25检索之前，根据伤员上下文硬过滤候选卡片集",
        "Post-retrieval（检索后）：对检索返回的卡片做冲突检测、优先级调整、升级方案注入",
        "Post-generation（生成后）：对LLM输出做剂量数值校验、必要步骤遗漏检测、告警注入",
    ]
    for s in stage_items:
        doc.add_bullet(s)
    doc.add_empty_line()
    
    doc.add_heading("3.4 示例规则", 2)
    for rule in SAMPLE_RULES:
        doc.add_paragraph(f"【{rule['rule_id']}】{rule['name']}", bold=True)
        doc.add_bullet(f"类型: {rule['rule_type']}  |  阶段: {rule['scope']}  |  优先级: {rule['priority']}")
        doc.add_bullet(f"条件: {rule['condition_desc']}")
        doc.add_bullet(f"动作: {rule['action']}")
        doc.add_bullet(f"告警消息: {rule['message']}")
        doc.add_bullet(f"依据: {rule['evidence']}")
        doc.add_empty_line()

    # ============================================================
    # 第四章：轻量关系模型Schema
    # ============================================================
    doc.add_heading("第四章  轻量关系模型Schema", 1)
    
    doc.add_heading("4.1 六类关系定义", 2)
    doc.add_paragraph(
        "本方法定义六类面向战创伤救护任务的轻量关系，替代完整知识图谱的三元组体系。"
        "关系仅在知识卡片之间建立，标注方式为在源卡片YAML中填写目标ID，成本极低。"
    )
    headers = ["关系类型", "中文名", "语义说明", "示例", "方向性", "调用用途"]
    rows = RELATION_TYPE_DEFINITIONS
    doc.add_table(headers, rows)
    
    doc.add_heading("4.2 完整JSON Schema定义", 2)
    doc.add_paragraph("以下为关系记录的JSON Schema：")
    doc.add_code_block(RELATION_SCHEMA_JSON.split('\n'))
    doc.add_empty_line()
    
    doc.add_heading("4.3 关系驱动的检索扩展策略", 2)
    doc.add_paragraph("根据查询意图的不同，系统使用不同的关系进行检索扩展：")
    expand_strategies = [
        ("流程类问题", "precedes + refines", "沿流程链展开前后步骤，并细化到具体操作"),
        ("替代方案问题", "alternatives", "当首选方案不可用时，通过alternatives关系找到等价替代"),
        ("升级/后送问题", "escalates_to", "当前处置无效时，向上追溯升级路径"),
        ("条件触发", "triggered_by", "根据伤员症状/体征触发对应的处置卡片"),
        ("冲突检测", "forbids_with", "不做扩展，而是检查已检索卡片集中的禁忌对"),
    ]
    doc.add_table(
        ["查询意图", "使用关系", "扩展策略"],
        expand_strategies
    )
    
    doc.add_paragraph("扩展伪代码：", bold=True)
    expand_code = [
        "def expand_with_relations(seed_cards, query_intent):",
        "    expanded = set(seed_cards)",
        "    for card in seed_cards:",
        "        if query_intent == 'step_by_step':",
        "            expanded |= neighbors(card, rel='precedes')",
        "            expanded |= neighbors(card, rel='refines', direction='out')",
        "        elif query_intent == 'alternative_plan':",
        "            expanded |= neighbors(card, rel='alternatives')",
        "        elif query_intent == 'escalation':",
        "            expanded |= neighbors(card, rel='escalates_to')",
        "    # forbids_with 不扩展，进入冲突检查",
        "    conflicts = detect_forbids(expanded)",
        "    return expanded, conflicts",
    ]
    doc.add_code_block(expand_code)
    doc.add_empty_line()
    
    doc.add_heading("4.4 示例关系", 2)
    headers = ["关系ID", "源卡片", "关系类型", "目标卡片", "说明"]
    doc.add_table(headers, SAMPLE_RELATIONS)

    # ============================================================
    # 第五章：一体化调用框架
    # ============================================================
    doc.add_heading("第五章  一体化调用框架设计", 1)
    
    doc.add_heading("5.1 系统架构", 2)
    doc.add_paragraph("系统分为三层：维护态（Authoring）、编译态（Build）、调用态（Runtime）。")
    arch_layers = [
        "维护态：医学专家使用 Markdown + YAML frontmatter 编写知识卡片，通过 Git 版本控制",
        "编译态：CI流水线执行 Schema校验 → MD解析 → JSONL生成 → 向量化 → 关系提取 → 规则校验",
        "调用态：接收用户查询，执行 Query理解 → Pre-rule → 混合检索 → 关系扩展 → Post-rule → LLM生成 → Post-gen校验",
    ]
    for l in arch_layers:
        doc.add_bullet(l)
    doc.add_empty_line()
    
    doc.add_heading("5.2 调用管线流程", 2)
    pipeline_steps = [
        "Step 1 - Query理解：LLM解析用户问题，提取意图(intent)、实体(entities)、MARCH阶段(stage)",
        "Step 2 - Pre-retrieval规则：根据伤员上下文执行pre_retrieval类规则，过滤不适用卡片",
        "Step 3 - 混合检索：BM25 + Dense Retrieval 并行召回，RRF融合得Top-20",
        "Step 4 - 关系扩展：根据query_intent使用对应关系类型扩展候选卡片集",
        "Step 5 - Post-retrieval规则：冲突检测(forbids_with对)、优先级调整、升级方案注入",
        "Step 6 - Cross-encoder重排：精排Top-8卡片作为上下文",
        "Step 7 - LLM生成：使用结构化Prompt模板，要求引用CARD-ID",
        "Step 8 - Post-generation规则：剂量校验、必要步骤检查、告警注入",
        "Step 9 - 输出：返回answer + citations[] + warnings[]",
    ]
    for s in pipeline_steps:
        doc.add_bullet(s)
    doc.add_empty_line()
    
    doc.add_heading("5.3 Prompt模板设计", 2)
    doc.add_paragraph("LLM生成阶段使用以下结构化Prompt：")
    prompt_template = [
        "你是战创伤急救辅助系统。严格基于下列知识卡片回答，并标注来源[CARD-ID]。",
        "",
        "# 伤员当前状态",
        "- MARCH阶段：{patient.march_stage}",
        "- 已执行处置：{patient.done_actions}",
        "- 已知禁忌：{patient.contraindications}",
        "",
        "# 可用知识卡片（已通过安全规则过滤）",
        "[CARD-HEM-TQ-001] 战术止血带（CAT）四肢大出血控制",
        "  摘要: ...",
        "  步骤: 1... 2... 3...",
        "  证据: TCCC Guidelines 2024, 3.a, Grade A",
        "",
        "[CARD-xxx] ...",
        "",
        "# 已自动排除的卡片（规则触发）",
        "- CARD-HEM-JOINT-TQ（原因：关节部位禁用CAT，规则R-HEM-001）",
        "",
        "# 回答要求",
        "1. 按MARCH优先级顺序组织回答",
        "2. 每条建议必须引用[CARD-ID]",
        "3. 时间敏感操作在开头标记【立即】",
        "4. 严禁推断卡片中未出现的剂量数值",
        "5. 如有禁忌冲突，优先执行安全规则的告警",
    ]
    doc.add_code_block(prompt_template)
    doc.add_empty_line()
    
    doc.add_paragraph("技术栈建议（全开源）：", bold=True)
    tech_stack = [
        ("源格式编辑", "VSCode + YAML插件 / Obsidian"),
        ("Schema校验", "jsonschema (Python)"),
        ("MD解析", "python-frontmatter + markdown-it-py"),
        ("向量化模型", "BGE-M3 / Piccolo-large-zh（医学微调）"),
        ("向量数据库", "Qdrant / Chroma（本地模式）"),
        ("BM25检索", "bm25s（纯Python实现）"),
        ("重排模型", "bge-reranker-v2-m3"),
        ("规则引擎", "json-logic-py"),
        ("LLM", "Qwen2.5-72B / DeepSeek-V3"),
        ("Runtime", "FastAPI + 自研Pipeline"),
    ]
    doc.add_table(["层", "推荐组件"], tech_stack)
    
    doc.add_empty_line()
    doc.add_paragraph("— 文档结束 —", bold=True)
    
    # 保存
    output_path = "/projects/sandbox/awesome-books/战创伤救护知识组织_Schema与评估框架.docx"
    doc.save(output_path)
    print(f"Word文档已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    main()
