#!/usr/bin/env python3
"""Append chapters 4-5 to the TXT document."""

OUTPUT = "/projects/sandbox/awesome-books/战创伤救护知识组织_Schema与评估框架.txt"

def main():
    lines = []
    def h1(t): lines.append(f"\n{'='*70}\n{t}\n{'='*70}\n")
    def h2(t): lines.append(f"\n{'─'*50}\n{t}\n{'─'*50}\n")
    def h3(t): lines.append(f"\n■ {t}\n")
    def p(t): lines.append(t)
    def bullet(t): lines.append(f"  • {t}")
    def blank(): lines.append("")
    def code(block):
        lines.append("  ┌─────────────────────────────────────────────────────────────")
        for l in block:
            lines.append(f"  │ {l}")
        lines.append("  └─────────────────────────────────────────────────────────────")

    # ==================== 第四章 ====================
    h1("第四章  轻量关系模型Schema")

    h2("4.1 六类关系定义")
    p("本方法定义六类面向战创伤救护任务的轻量关系，替代完整知识图谱的三元组体系。")
    p("关系仅在知识卡片之间建立，标注方式为在源卡片YAML中填写目标ID，成本极低。")
    blank()
    p(f"{'关系类型':<16} {'中文名':<8} {'语义说明':<30} {'方向性':<12} 调用用途")
    p("-" * 110)
    rels = [
        ("precedes","流程编排","A在处置流程上先于B执行","单向","确定处置顺序，生成多步应答"),
        ("triggered_by","条件触发","当条件C满足时触发执行卡A","单向","症状→处置映射，条件分支"),
        ("alternatives","替代路径","A与B功能等价可互相替代","双向","资源不可用时自动切换"),
        ("refines","细化展开","A是B的细化子步骤","单向(父→子)","从总览深入到具体操作"),
        ("forbids_with","禁忌检测","A与B不能同时应用","双向","自动检测处置冲突告警"),
        ("escalates_to","升级指引","A不奏效时升级到B","单向","失败后的升级路径"),
    ]
    for r in rels:
        p(f"{r[0]:<16} {r[1]:<8} {r[2]:<30} {r[3]:<12} {r[4]}")
    blank()

    h2("4.2 完整JSON Schema定义")
    p("关系记录 JSON Schema:")
    blank()
    rel_schema = [
        '{',
        '  "$schema": "http://json-schema.org/draft-07/schema#",',
        '  "title": "KnowledgeRelation",',
        '  "description": "知识卡片间的轻量关系模型",',
        '  "type": "object",',
        '  "required": ["relation_id","src","rel_type","dst"],',
        '  "properties": {',
        '    "relation_id": {',
        '      "type": "string",',
        '      "pattern": "^REL-[0-9]{4}$",',
        '      "description": "关系唯一标识"',
        '    },',
        '    "src": {',
        '      "type": "string",',
        '      "description": "源卡片ID"',
        '    },',
        '    "rel_type": {',
        '      "type": "string",',
        '      "enum": ["precedes","triggered_by","alternatives","refines","forbids_with","escalates_to"],',
        '      "description": "关系类型（六类之一）"',
        '    },',
        '    "dst": {',
        '      "type": "string",',
        '      "description": "目标卡片ID（或条件ID）"',
        '    },',
        '    "bidirectional": {',
        '      "type": "boolean",',
        '      "default": false,',
        '      "description": "是否双向（alternatives和forbids_with默认true）"',
        '    },',
        '    "condition": {',
        '      "type": "string",',
        '      "description": "关系生效条件（可选）"',
        '    },',
        '    "weight": {',
        '      "type": "number",',
        '      "minimum": 0, "maximum": 1,',
        '      "default": 1.0,',
        '      "description": "关系权重，检索扩展时的置信度排序"',
        '    },',
        '    "annotation": {',
        '      "type": "string",',
        '      "description": "关系标注说明"',
        '    },',
        '    "evidence": {',
        '      "type": "object",',
        '      "properties": {',
        '        "source": {"type": "string"},',
        '        "section": {"type": "string"}',
        '      }',
        '    }',
        '  }',
        '}',
    ]
    code(rel_schema)
    blank()

    h2("4.3 关系驱动的检索扩展策略")
    p("根据查询意图使用不同关系进行检索扩展：")
    blank()
    p(f"{'查询意图':<16} {'使用关系':<24} 扩展策略")
    p("-" * 80)
    strategies = [
        ("流程类问题","precedes + refines","沿流程链展开前后步骤并细化到具体操作"),
        ("替代方案问题","alternatives","首选方案不可用时通过alternatives找等价替代"),
        ("升级/后送问题","escalates_to","当前处置无效时向上追溯升级路径"),
        ("条件触发","triggered_by","根据伤员症状/体征触发对应处置卡片"),
        ("冲突检测","forbids_with","检查已检索卡片集中的禁忌对（不做扩展）"),
    ]
    for s in strategies:
        p(f"{s[0]:<16} {s[1]:<24} {s[2]}")
    blank()

    p("扩展伪代码：")
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
    code(expand_code)
    blank()

    h2("4.4 示例关系")
    p(f"{'关系ID':<10} {'源卡片':<20} {'关系类型':<14} {'目标卡片':<24} 说明")
    p("-" * 110)
    sample_rels = [
        ("REL-0001","CARD-HEM-TQ-001","precedes","CARD-HEM-WOUND-002","止血带控制后进行伤口包扎"),
        ("REL-0002","CARD-HEM-TQ-001","alternatives","CARD-HEM-PRESSURE-003","直接加压可替代(非大出血)"),
        ("REL-0003","CARD-HEM-TQ-001","forbids_with","CARD-HEM-JOINT-TQ","标准CAT与关节部位止血不兼容"),
        ("REL-0004","CARD-HEM-TQ-001","escalates_to","CARD-EVAC-URGENT","止血带无效时升级到紧急后送"),
        ("REL-0005","CARD-MARCH-H-OVERVIEW","refines","CARD-HEM-TQ-001","H环节总览细化到止血带操作"),
        ("REL-0006","CARD-AIR-NPA-001","precedes","CARD-AIR-RECOVERY-001","NPA置入后摆放恢复体位"),
        ("REL-0007","CARD-AIR-NPA-001","alternatives","CARD-AIR-CRIC-001","NPA无法通气时考虑环甲膜切开"),
        ("REL-0008","CARD-AIR-NPA-001","escalates_to","CARD-AIR-CRIC-001","NPA失败则升级到外科气道"),
        ("REL-0009","CARD-DRUG-TXA-001","triggered_by","COND-MAJOR-HEMORRHAGE","大出血条件触发TXA给药"),
        ("REL-0010","CARD-DRUG-TXA-001","precedes","CARD-FLUID-RESUS-001","TXA给药先于液体复苏"),
    ]
    for r in sample_rels:
        p(f"{r[0]:<10} {r[1]:<20} {r[2]:<14} {r[3]:<24} {r[4]}")
    blank()

    # ==================== 第五章 ====================
    h1("第五章  一体化调用框架设计")

    h2("5.1 系统架构")
    p("系统分为三层：维护态（Authoring）、编译态（Build）、调用态（Runtime）。")
    blank()
    bullet("维护态：医学专家使用 Markdown + YAML frontmatter 编写知识卡片，通过 Git 版本控制")
    bullet("编译态：CI流水线执行 Schema校验 → MD解析 → JSONL生成 → 向量化 → 关系提取 → 规则校验")
    bullet("调用态：Query理解 → Pre-rule → 混合检索 → 关系扩展 → Post-rule → LLM生成 → Post-gen校验")
    blank()

    p("架构图（文本表示）：")
    arch = [
        "┌───────────────────────────────────────────────────────────────────┐",
        "│  维护态 (Authoring Layer)                                         │",
        "│  专家 → VSCode/Obsidian 编辑 .md (YAML frontmatter + 正文)        │",
        "│         ↓  git 提交                                               │",
        "│  CI: schema 校验 + lint + ID 唯一性检查                           │",
        "└───────────────────────────────────────────────────────────────────┘",
        "                         │ build.py (编译器)",
        "                         ▼",
        "┌───────────────────────────────────────────────────────────────────┐",
        "│  编译态 (Build Layer)                                             │",
        "│  .md → cards.jsonl   (知识卡片)                                   │",
        "│       → relations.jsonl (六类关系边)                              │",
        "│       → rules.jsonl  (外置安全规则)                               │",
        "│       → embeddings.parquet (向量)                                 │",
        "└───────────────────────────────────────────────────────────────────┘",
        "                         │",
        "                         ▼",
        "┌───────────────────────────────────────────────────────────────────┐",
        "│  调用态 (Runtime Layer)                                           │",
        "│  Query → [Pre-rule] → [BM25+向量] → [关系扩展] → [Post-rule]     │",
        "│        → [LLM生成] → [Post-gen校验] → 带证据链的回答              │",
        "└───────────────────────────────────────────────────────────────────┘",
    ]
    for l in arch:
        p(f"    {l}")
    blank()

    h2("5.2 调用管线流程")
    p("端到端调用管线9步：")
    blank()
    steps = [
        "Step 1 - Query理解：LLM解析用户问题，提取intent、entities、MARCH stage",
        "Step 2 - Pre-retrieval规则：根据伤员上下文执行pre_retrieval类规则，过滤不适用卡片",
        "Step 3 - 混合检索：BM25 + Dense Retrieval并行召回，RRF融合得Top-20",
        "Step 4 - 关系扩展：根据query_intent使用对应关系类型扩展候选卡片集",
        "Step 5 - Post-retrieval规则：冲突检测(forbids_with对)、优先级调整、升级方案注入",
        "Step 6 - Cross-encoder重排：精排Top-8卡片作为上下文",
        "Step 7 - LLM生成：使用结构化Prompt模板，要求引用CARD-ID",
        "Step 8 - Post-generation规则：剂量校验、必要步骤检查、告警注入",
        "Step 9 - 输出：返回 {answer, citations[], warnings[]}",
    ]
    for s in steps:
        bullet(s)
    blank()

    p("管线伪代码：")
    pipeline_code = [
        "def answer(user_query, patient_ctx):",
        "    intent = parse_intent(user_query)  # LLM轻量parse",
        "    ",
        "    # Pre-rule",
        "    excluded = apply_rules(rules, stage='pre', ctx=patient_ctx)",
        "    ",
        "    # 混合检索",
        "    bm25_hits  = bm25.search(user_query, exclude=excluded)",
        "    dense_hits = vec.search(user_query, exclude=excluded)",
        "    fused = rrf_fuse(bm25_hits, dense_hits, k=20)",
        "    ",
        "    # 关系扩展",
        "    cards = expand_with_relations(fused, intent.type)",
        "    ",
        "    # Post-retrieval规则",
        "    cards = apply_rules(rules, stage='post_retrieval', cards=cards)",
        "    cards = rerank(cards, user_query, top_k=8)",
        "    ",
        "    # LLM生成",
        "    draft = llm.generate(build_prompt(user_query, cards, patient_ctx))",
        "    ",
        "    # Post-generation规则",
        "    final = apply_rules(rules, stage='post_gen', answer=draft)",
        "    ",
        "    return {answer: final.text, citations: final.cites, warnings: final.warnings}",
    ]
    code(pipeline_code)
    blank()

    h2("5.3 Prompt模板设计")
    p("LLM生成阶段使用以下结构化Prompt：")
    blank()
    prompt = [
        "你是战创伤急救辅助系统。严格基于下列知识卡片回答，并标注来源[CARD-ID]。",
        "",
        "# 伤员当前状态",
        "- MARCH阶段：{patient.march_stage}",
        "- 已执行处置：{patient.done_actions}",
        "- 已知禁忌：{patient.contraindications}",
        "",
        "# 可用知识卡片（已通过安全规则过滤）",
        "[CARD-HEM-TQ-001] 战术止血带（CAT）四肢大出血控制",
        "  摘要: 对四肢大出血使用CAT止血带进行紧急止血",
        "  步骤: 1.识别出血 2.取出CAT 3.置于近心端5-7cm 4.拉紧 5.旋转绞棒 6.固定 7.标记时间 8.暴露",
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
    code(prompt)
    blank()

    p("技术栈建议（全开源）：")
    blank()
    p(f"{'层':<16} 推荐组件")
    p("-" * 60)
    stack = [
        ("源格式编辑","VSCode + YAML插件 / Obsidian"),
        ("Schema校验","jsonschema (Python)"),
        ("MD解析","python-frontmatter + markdown-it-py"),
        ("向量化模型","BGE-M3 / Piccolo-large-zh（医学微调）"),
        ("向量数据库","Qdrant / Chroma（本地模式）"),
        ("BM25检索","bm25s（纯Python实现）"),
        ("重排模型","bge-reranker-v2-m3"),
        ("规则引擎","json-logic-py"),
        ("LLM","Qwen2.5-72B / DeepSeek-V3"),
        ("Runtime","FastAPI + 自研Pipeline"),
    ]
    for s in stack:
        p(f"{s[0]:<16} {s[1]}")
    blank()

    p("=" * 70)
    p("— 文档结束 —")
    p("=" * 70)

    with open(OUTPUT, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Part 3 appended: {len(lines)} lines")

if __name__ == "__main__":
    main()
