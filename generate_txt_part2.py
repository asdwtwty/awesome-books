#!/usr/bin/env python3
"""Append chapters 2-5 to the TXT document."""

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

    # ==================== 第二章 ====================
    h1("第二章  知识卡片模型Schema")

    h2("2.1 设计原则")
    bullet("一卡一动作/一概念：每张卡片对应TCCC/PFC中一个可独立问答的最小知识单元")
    bullet("语义自足：卡片脱离上下文仍可理解，body.summary字段必填")
    bullet("可独立验证：每卡至少一条evidence来源，支持溯源审计")
    bullet("双表示统一：YAML frontmatter为人工维护态，JSON为机器调用态，编译器保证一致性")
    bullet("类型区分：5种task_type对应不同必填字段，Schema层面强制约束")
    blank()

    h2("2.2 完整JSON Schema定义")
    p("知识卡片 JSON Schema (draft-07):")
    blank()
    card_schema = [
        '{',
        '  "$schema": "http://json-schema.org/draft-07/schema#",',
        '  "title": "KnowledgeCard",',
        '  "description": "战创伤救护知识卡片模型 - 面向RAG的最小知识单元",',
        '  "type": "object",',
        '  "required": ["id","title","version","updated","module","phase","task_type","body","evidence"],',
        '  "properties": {',
        '    "id": {',
        '      "type": "string",',
        '      "pattern": "^CARD-[A-Z]{2,6}-[A-Z0-9]+-[0-9]{3}$",',
        '      "description": "全局唯一标识，格式: CARD-{模块}-{简写}-{序号}"',
        '    },',
        '    "title": {',
        '      "type": "string",',
        '      "maxLength": 80,',
        '      "description": "卡片标题，一句话概括本卡主题"',
        '    },',
        '    "version": {',
        '      "type": "string",',
        '      "pattern": "^[0-9]+\\\\.[0-9]+\\\\.[0-9]+$",',
        '      "description": "语义版本号 major.minor.patch"',
        '    },',
        '    "updated": {',
        '      "type": "string",',
        '      "format": "date",',
        '      "description": "最后更新日期 YYYY-MM-DD"',
        '    },',
        '    "authors": {',
        '      "type": "array",',
        '      "items": {"type": "string"},',
        '      "description": "编写/审核人员列表"',
        '    },',
        '    "module": {',
        '      "type": "string",',
        '      "enum": ["MARCH.M","MARCH.A","MARCH.R","MARCH.C","MARCH.H",',
        '               "PAWS.P","PAWS.A","PAWS.W","PAWS.S",',
        '               "PFC.HITMAN","PFC.SHEEPVOMIT","PFC.GENERAL"],',
        '      "description": "所属模块：MARCH五环节 / PAWS四环节 / PFC延续救护"',
        '    },',
        '    "phase": {',
        '      "type": "string",',
        '      "enum": ["CUF","TFC","TACEVAC","PFC"],',
        '      "description": "适用阶段: Care Under Fire / Tactical Field Care / TACEVAC / PFC"',
        '    },',
        '    "task_type": {',
        '      "type": "string",',
        '      "enum": ["procedure","decision","knowledge","drug","equipment"],',
        '      "description": "卡片类型：操作流程/决策判断/知识概念/药物/器材"',
        '    },',
        '    "applicable_to": {',
        '      "type": "array",',
        '      "items": {"type": "string"},',
        '      "description": "适应证/适用场景标签列表"',
        '    },',
        '    "contraindications": {',
        '      "type": "array",',
        '      "items": {"type": "string"},',
        '      "description": "禁忌证标签列表"',
        '    },',
        '    "patient_group": {',
        '      "type": "array",',
        '      "items": {"type": "string", "enum": ["adult","pediatric","pregnant","geriatric","burn"]},',
        '      "description": "适用人群"',
        '    },',
        '    "body": {',
        '      "type": "object",',
        '      "description": "卡片正文结构化内容",',
        '      "required": ["summary"],',
        '      "properties": {',
        '        "summary": {"type": "string", "description": "一句话摘要"},',
        '        "indication": {"type": "string", "description": "适应证描述"},',
        '        "steps": {',
        '          "type": "array",',
        '          "items": {"type": "string"},',
        '          "description": "操作步骤（procedure类型必填）"',
        '        },',
        '        "criteria": {',
        '          "type": "array",',
        '          "items": {"type": "string"},',
        '          "description": "判断标准（decision类型必填）"',
        '        },',
        '        "dosage": {',
        '          "type": "object",',
        '          "properties": {',
        '            "dose": {"type": "string"},',
        '            "route": {"type": "string", "enum": ["IV","IO","IM","PO","IN","topical"]},',
        '            "frequency": {"type": "string"},',
        '            "max_dose": {"type": "string"}',
        '          },',
        '          "description": "用药方案（drug类型必填）"',
        '        },',
        '        "notes": {',
        '          "type": "array",',
        '          "items": {"type": "string"},',
        '          "description": "注意事项"',
        '        },',
        '        "definition": {"type": "string", "description": "概念定义（knowledge类型）"},',
        '        "mechanism": {"type": "string", "description": "机理说明"},',
        '        "specification": {',
        '          "type": "object",',
        '          "description": "器材规格（equipment类型）",',
        '          "properties": {',
        '            "model": {"type": "string"},',
        '            "sizes": {"type": "array", "items": {"type": "string"}},',
        '            "weight": {"type": "string"}',
        '          }',
        '        }',
        '      }',
        '    },',
        '    "evidence": {',
        '      "type": "array",',
        '      "minItems": 1,',
        '      "items": {',
        '        "type": "object",',
        '        "required": ["source","section"],',
        '        "properties": {',
        '          "source": {"type": "string"},',
        '          "section": {"type": "string"},',
        '          "url": {"type": "string", "format": "uri"},',
        '          "grade": {"type": "string", "enum": ["A","B","C","D","expert_opinion"]}',
        '        }',
        '      },',
        '      "description": "证据来源（至少一条）"',
        '    },',
        '    "tags": {',
        '      "type": "array",',
        '      "items": {"type": "string"},',
        '      "description": "检索标签（同义词、关键术语）"',
        '    },',
        '    "related": {',
        '      "type": "object",',
        '      "description": "六类轻量关系引用",',
        '      "properties": {',
        '        "precedes": {"type": "array", "items": {"type": "string"}},',
        '        "triggered_by": {"type": "array", "items": {"type": "string"}},',
        '        "alternatives": {"type": "array", "items": {"type": "string"}},',
        '        "refines": {"type": "array", "items": {"type": "string"}},',
        '        "forbids_with": {"type": "array", "items": {"type": "string"}},',
        '        "escalates_to": {"type": "array", "items": {"type": "string"}}',
        '      }',
        '    },',
        '    "hash": {',
        '      "type": "string",',
        '      "description": "内容SHA-256哈希，用于防篡改校验"',
        '    }',
        '  }',
        '}',
    ]
    code(card_schema)
    blank()

    h2("2.3 字段说明表")
    p(f"{'字段':<20} {'类型':<16} {'必填':<14} 说明")
    p("-" * 100)
    fields = [
        ("id","string","是","全局唯一标识，格式CARD-{模块}-{简写}-{序号}"),
        ("title","string","是","卡片标题，<=80字符"),
        ("version","string","是","语义版本号 major.minor.patch"),
        ("updated","date","是","最后更新日期"),
        ("authors","array[string]","否","编写/审核人员"),
        ("module","enum","是","所属MARCH/PAWS/PFC模块"),
        ("phase","enum","是","适用救治阶段CUF/TFC/TACEVAC/PFC"),
        ("task_type","enum","是","卡片类型：procedure/decision/knowledge/drug/equipment"),
        ("applicable_to","array[string]","否","适应证标签"),
        ("contraindications","array[string]","否","禁忌证标签"),
        ("patient_group","array[enum]","否","适用人群"),
        ("body.summary","string","是","一句话摘要"),
        ("body.steps","array[string]","procedure必填","操作步骤"),
        ("body.criteria","array[string]","decision必填","判断标准"),
        ("body.dosage","object","drug必填","剂量/途径/频次/上限"),
        ("body.notes","array[string]","否","注意事项"),
        ("evidence","array[object]","是","至少一条证据来源+等级"),
        ("tags","array[string]","否","检索标签/同义词"),
        ("related","object","否","六类关系引用"),
        ("hash","string","自动生成","内容SHA-256防篡改"),
    ]
    for f in fields:
        p(f"{f[0]:<20} {f[1]:<16} {f[2]:<14} {f[3]}")
    blank()

    h2("2.4 示例卡片")
    blank()
    p("【CARD-HEM-TQ-001】战术止血带（CAT）四肢大出血控制")
    p("─" * 40)
    bullet("模块: MARCH.M  |  阶段: CUF  |  类型: procedure")
    bullet("摘要: 对四肢大出血使用CAT止血带进行紧急止血")
    p("  操作步骤：")
    bullet("1. 识别四肢活动性大出血（喷射状/涌出/浸透敷料）")
    bullet("2. 取出CAT Gen 7止血带，拉出自由端")
    bullet("3. 将止血带置于出血点近心端5-7cm处（CUF阶段：高位放置）")
    bullet("4. 拉紧自由端穿过扣环并回折粘贴")
    bullet("5. 旋转绞棒直至出血停止且远端脉搏消失")
    bullet("6. 将绞棒固定在卡夹中")
    bullet("7. 用记号笔在止血带上标记上带时间")
    bullet("8. 暴露止血带（不得被衣物遮盖）")
    bullet("禁忌证: 关节部位（膝/肘）、颈部/躯干")
    bullet("证据: TCCC Guidelines 2024, Section 3.a; CoTCCC Recommendation 2020-01, Grade A")
    blank()

    p("【CARD-DRUG-TXA-001】氨甲环酸（TXA）抗纤溶治疗")
    p("─" * 40)
    bullet("模块: MARCH.C  |  阶段: TFC  |  类型: drug")
    bullet("摘要: 对预计需要大量输血或合并TBI的伤员给予TXA减少出血")
    bullet("用药方案: 2g IV/IO 缓慢推注（10分钟以上）；如无IV/IO通路可IM给药")
    bullet("适应证: 预计需要大量输血的创伤伤员；合并显著TBI的伤员")
    bullet("禁忌证: 受伤超过3小时、已知对TXA过敏")
    bullet("证据: TCCC Guidelines 2024 Proposed Change 20-02; MATTERs Study, Grade A")
    blank()

    p("【CARD-AIR-NPA-001】鼻咽通气道（NPA）置入")
    p("─" * 40)
    bullet("模块: MARCH.A  |  阶段: TFC  |  类型: procedure")
    bullet("摘要: 对有自主呼吸但意识障碍的伤员建立鼻咽通气道")
    p("  操作步骤：")
    bullet("1. 评估伤员：有自主呼吸、GCS<=13或打鼾样呼吸")
    bullet("2. 选择合适尺寸NPA（成人通常28F）")
    bullet("3. 润滑NPA外壁")
    bullet("4. 斜面朝向鼻中隔，沿鼻底方向缓慢插入")
    bullet("5. 确认气道通畅（听诊呼吸音、观察胸廓起伏）")
    bullet("禁忌证: 严重颌面部创伤、已知颅底骨折")
    bullet("证据: TCCC Guidelines 2024, Airway Management; Grade B")
    blank()

    # ==================== 第三章 ====================
    h1("第三章  安全规则层Schema")

    h2("3.1 设计原则")
    bullet("外置化：安全约束独立于知识正文存储和执行，不依赖LLM理解自然语言中的禁忌")
    bullet("多阶段执行：规则可在检索前/检索后/生成后三阶段分别触发")
    bullet("声明式条件：使用JSON-Logic语法，可被程序自动求值")
    bullet("优先级仲裁：冲突规则按priority字段排序，高优先级覆盖低优先级")
    bullet("证据溯源：每条规则必须标注依据来源")
    bullet("可开关：enabled字段支持灰度发布和AB测试")
    blank()

    h2("3.2 完整JSON Schema定义")
    p("安全规则 JSON Schema:")
    blank()
    rule_schema = [
        '{',
        '  "$schema": "http://json-schema.org/draft-07/schema#",',
        '  "title": "SafetyRule",',
        '  "description": "安全约束外置化规则 - 独立于知识正文执行的硬约束",',
        '  "type": "object",',
        '  "required": ["rule_id","rule_type","scope","priority","condition","action","evidence"],',
        '  "properties": {',
        '    "rule_id": {',
        '      "type": "string",',
        '      "pattern": "^R-[A-Z]{2,6}-[0-9]{3}$",',
        '      "description": "规则唯一标识，格式: R-{类别}-{序号}"',
        '    },',
        '    "rule_type": {',
        '      "type": "string",',
        '      "enum": ["contraindication","priority_override","escalation_trigger",',
        '               "dosage_bound","time_constraint","combination_forbidden"],',
        '      "description": "规则类型"',
        '    },',
        '    "scope": {',
        '      "type": "string",',
        '      "enum": ["pre_retrieval","post_retrieval","post_generation","all_stages"],',
        '      "description": "执行阶段"',
        '    },',
        '    "priority": {',
        '      "type": "integer",',
        '      "minimum": 1, "maximum": 100,',
        '      "description": "优先级（1=最高）"',
        '    },',
        '    "name": {"type": "string", "description": "规则名称"},',
        '    "description": {"type": "string", "description": "规则说明"},',
        '    "condition": {',
        '      "type": "object",',
        '      "required": ["logic"],',
        '      "properties": {',
        '        "logic": {',
        '          "type": "object",',
        '          "description": "JSON-Logic表达式"',
        '        },',
        '        "variables": {',
        '          "type": "array",',
        '          "items": {',
        '            "type": "object",',
        '            "properties": {',
        '              "name": {"type": "string"},',
        '              "source": {"type": "string",',
        '                "enum": ["patient_context","query","retrieved_cards","generated_text"]},',
        '              "path": {"type": "string"}',
        '            }',
        '          }',
        '        }',
        '      }',
        '    },',
        '    "action": {',
        '      "type": "object",',
        '      "required": ["type"],',
        '      "properties": {',
        '        "type": {',
        '          "type": "string",',
        '          "enum": ["exclude_cards","include_cards","rerank_boost","rerank_penalize",',
        '                   "inject_warning","block_generation","rewrite_answer","add_citation"]',
        '        },',
        '        "targets": {"type": "array", "items": {"type": "string"}},',
        '        "message": {"type": "string"},',
        '        "severity": {"type": "string", "enum": ["critical","warning","info"]}',
        '      }',
        '    },',
        '    "evidence": {',
        '      "type": "object",',
        '      "required": ["source"],',
        '      "properties": {',
        '        "source": {"type": "string"},',
        '        "section": {"type": "string"},',
        '        "grade": {"type": "string", "enum": ["A","B","C","D","expert_opinion"]}',
        '      }',
        '    },',
        '    "enabled": {"type": "boolean", "default": true},',
        '    "version": {"type": "string"}',
        '  }',
        '}',
    ]
    code(rule_schema)
    blank()

    h2("3.3 规则类型与执行阶段")
    p(f"{'类型标识':<24} {'中文名':<10} {'典型执行阶段':<16} 功能说明")
    p("-" * 100)
    rtypes = [
        ("contraindication","禁忌证","pre_retrieval","根据伤员状态排除不适用的知识卡片"),
        ("priority_override","优先级覆盖","post_retrieval","根据伤情紧急程度调整卡片排序"),
        ("escalation_trigger","升级触发","post_retrieval","当前处置无效时自动引入升级方案"),
        ("dosage_bound","剂量边界","post_generation","校验LLM输出的药物剂量是否在允许范围"),
        ("time_constraint","时间约束","post_retrieval","超出时间窗的处置予以排除"),
        ("combination_forbidden","联合禁忌","post_retrieval","检测多卡片间的禁忌组合"),
    ]
    for r in rtypes:
        p(f"{r[0]:<24} {r[1]:<10} {r[2]:<16} {r[3]}")
    blank()
    p("三阶段执行时序：")
    bullet("Pre-retrieval（检索前）：根据伤员上下文硬过滤候选卡片集")
    bullet("Post-retrieval（检索后）：冲突检测、优先级调整、升级方案注入")
    bullet("Post-generation（生成后）：剂量数值校验、必要步骤遗漏检测、告警注入")
    blank()

    h2("3.4 示例规则")
    rules = [
        ("R-HEM-001","关节部位禁用止血带","contraindication","pre_retrieval",5,
         "patient.injury_site IN ['膝关节','肘关节','关节']","exclude_cards: [CARD-HEM-TQ-001]",
         "关节部位不适用止血带，应改用加压包扎或止血填塞","TCCC Guidelines 2024, 3.a"),
        ("R-DRUG-001","TXA时间窗约束","time_constraint","post_retrieval",3,
         "patient.time_since_injury > 3h","exclude_cards + inject_warning",
         "受伤超过3小时，TXA获益不确定且可能增加风险","CRASH-2 Trial; TCCC 20-02"),
        ("R-DOSE-001","TXA剂量上限校验","dosage_bound","post_generation",2,
         "generated_text中TXA剂量 > 2g","inject_warning + rewrite_answer",
         "TXA单次剂量不应超过2g","TCCC Guidelines 2024"),
        ("R-ESC-001","止血带失效升级","escalation_trigger","post_retrieval",8,
         "patient.tourniquet_applied AND bleeding_continues","include_cards: [CARD-EVAC-URGENT]",
         "止血带未能控制出血，应考虑交界区止血器材或紧急后送","TCCC Guidelines 2024, 3.c"),
    ]
    for r in rules:
        p(f"【{r[0]}】{r[1]}")
        bullet(f"类型: {r[2]}  |  阶段: {r[3]}  |  优先级: {r[4]}")
        bullet(f"条件: {r[5]}")
        bullet(f"动作: {r[6]}")
        bullet(f"告警: {r[7]}")
        bullet(f"依据: {r[8]}")
        blank()

    # Append to file
    with open(OUTPUT, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Part 2 appended: {len(lines)} lines")

if __name__ == "__main__":
    main()
