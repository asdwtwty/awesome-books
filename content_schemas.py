"""
Schema definitions for TCCC/PFC knowledge organization system.
"""

CARD_SCHEMA_JSON = '''{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KnowledgeCard",
  "description": "战创伤救护知识卡片模型 - 面向RAG的最小知识单元",
  "type": "object",
  "required": ["id","title","version","updated","module","phase","task_type","body","evidence"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^CARD-[A-Z]{2,6}-[A-Z0-9]+-[0-9]{3}$",
      "description": "全局唯一标识，格式: CARD-{模块}-{简写}-{序号}，如 CARD-HEM-TQ-001"
    },
    "title": {
      "type": "string",
      "maxLength": 80,
      "description": "卡片标题，一句话概括本卡主题"
    },
    "version": {
      "type": "string",
      "pattern": "^[0-9]+\\\\.[0-9]+\\\\.[0-9]+$",
      "description": "语义版本号 major.minor.patch"
    },
    "updated": {
      "type": "string",
      "format": "date",
      "description": "最后更新日期 YYYY-MM-DD"
    },
    "authors": {
      "type": "array",
      "items": {"type": "string"},
      "description": "编写/审核人员列表"
    },
    "module": {
      "type": "string",
      "enum": ["MARCH.M","MARCH.A","MARCH.R","MARCH.C","MARCH.H",
               "PAWS.P","PAWS.A","PAWS.W","PAWS.S",
               "PFC.HITMAN","PFC.SHEEPVOMIT","PFC.GENERAL"],
      "description": "所属模块：MARCH五环节 / PAWS四环节 / PFC延续救护"
    },
    "phase": {
      "type": "string",
      "enum": ["CUF","TFC","TACEVAC","PFC"],
      "description": "适用阶段: Care Under Fire / Tactical Field Care / Tactical Evacuation Care / Prolonged Field Care"
    },
    "task_type": {
      "type": "string",
      "enum": ["procedure","decision","knowledge","drug","equipment"],
      "description": "卡片类型：操作流程/决策判断/知识概念/药物/器材"
    },
    "applicable_to": {
      "type": "array",
      "items": {"type": "string"},
      "description": "适应证/适用场景标签列表"
    },
    "contraindications": {
      "type": "array",
      "items": {"type": "string"},
      "description": "禁忌证标签列表"
    },
    "patient_group": {
      "type": "array",
      "items": {"type": "string","enum": ["adult","pediatric","pregnant","geriatric","burn"]},
      "description": "适用人群"
    },
    "body": {
      "type": "object",
      "description": "卡片正文结构化内容",
      "properties": {
        "summary": {"type": "string", "description": "一句话摘要（LLM自动生成或人工填写）"},
        "indication": {"type": "string", "description": "适应证描述"},
        "steps": {
          "type": "array",
          "items": {"type": "string"},
          "description": "操作步骤（procedure类型必填）"
        },
        "criteria": {
          "type": "array",
          "items": {"type": "string"},
          "description": "判断标准（decision类型必填）"
        },
        "dosage": {
          "type": "object",
          "properties": {
            "dose": {"type": "string"},
            "route": {"type": "string","enum": ["IV","IO","IM","PO","IN","topical"]},
            "frequency": {"type": "string"},
            "max_dose": {"type": "string"}
          },
          "description": "用药方案（drug类型必填）"
        },
        "notes": {
          "type": "array",
          "items": {"type": "string"},
          "description": "注意事项"
        },
        "definition": {"type": "string", "description": "概念定义（knowledge类型）"},
        "mechanism": {"type": "string", "description": "机理说明"},
        "specification": {
          "type": "object",
          "description": "器材规格（equipment类型）",
          "properties": {
            "model": {"type": "string"},
            "sizes": {"type": "array","items": {"type": "string"}},
            "weight": {"type": "string"}
          }
        }
      },
      "required": ["summary"]
    },
    "evidence": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["source","section"],
        "properties": {
          "source": {"type": "string", "description": "文献/指南名称"},
          "section": {"type": "string", "description": "章节/页码"},
          "url": {"type": "string", "format": "uri"},
          "grade": {"type": "string", "enum": ["A","B","C","D","expert_opinion"],
                    "description": "证据等级"}
        }
      },
      "description": "证据来源（至少一条）"
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "description": "检索标签（同义词、关键术语）"
    },
    "related": {
      "type": "object",
      "description": "六类轻量关系引用",
      "properties": {
        "precedes": {"type": "array","items": {"type": "string"}},
        "triggered_by": {"type": "array","items": {"type": "string"}},
        "alternatives": {"type": "array","items": {"type": "string"}},
        "refines": {"type": "array","items": {"type": "string"}},
        "forbids_with": {"type": "array","items": {"type": "string"}},
        "escalates_to": {"type": "array","items": {"type": "string"}}
      }
    },
    "hash": {
      "type": "string",
      "description": "内容SHA-256哈希，用于防篡改校验"
    }
  }
}'''

RULE_SCHEMA_JSON = '''{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SafetyRule",
  "description": "安全约束外置化规则 - 独立于知识正文执行的硬约束",
  "type": "object",
  "required": ["rule_id","rule_type","scope","priority","condition","action","evidence"],
  "properties": {
    "rule_id": {
      "type": "string",
      "pattern": "^R-[A-Z]{2,6}-[0-9]{3}$",
      "description": "规则唯一标识，格式: R-{类别}-{序号}"
    },
    "rule_type": {
      "type": "string",
      "enum": ["contraindication","priority_override","escalation_trigger",
               "dosage_bound","time_constraint","combination_forbidden"],
      "description": "规则类型：禁忌证/优先级覆盖/升级触发/剂量边界/时间约束/联合禁忌"
    },
    "scope": {
      "type": "string",
      "enum": ["pre_retrieval","post_retrieval","post_generation","all_stages"],
      "description": "执行阶段：检索前/检索后/生成后/全阶段"
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "description": "优先级（1=最高），冲突时高优先级覆盖低优先级"
    },
    "name": {
      "type": "string",
      "description": "规则名称，人类可读"
    },
    "description": {
      "type": "string",
      "description": "规则说明，解释为何需要此约束"
    },
    "condition": {
      "type": "object",
      "description": "触发条件，使用JSON-Logic语法",
      "properties": {
        "logic": {
          "type": "object",
          "description": "JSON-Logic表达式，支持 and/or/not/if/==/>/</in/var 等操作"
        },
        "variables": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "source": {"type": "string","enum": ["patient_context","query","retrieved_cards","generated_text"]},
              "path": {"type": "string"}
            }
          },
          "description": "条件中引用的变量定义"
        }
      },
      "required": ["logic"]
    },
    "action": {
      "type": "object",
      "description": "规则触发后的执行动作",
      "required": ["type"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["exclude_cards","include_cards","rerank_boost","rerank_penalize",
                   "inject_warning","block_generation","rewrite_answer","add_citation"],
          "description": "动作类型"
        },
        "targets": {
          "type": "array",
          "items": {"type": "string"},
          "description": "动作目标卡片ID列表"
        },
        "message": {
          "type": "string",
          "description": "警示/覆盖消息内容"
        },
        "severity": {
          "type": "string",
          "enum": ["critical","warning","info"],
          "description": "告警级别"
        }
      }
    },
    "evidence": {
      "type": "object",
      "properties": {
        "source": {"type": "string"},
        "section": {"type": "string"},
        "grade": {"type": "string","enum": ["A","B","C","D","expert_opinion"]}
      },
      "required": ["source"],
      "description": "规则依据来源"
    },
    "enabled": {
      "type": "boolean",
      "default": true,
      "description": "是否启用"
    },
    "version": {
      "type": "string",
      "description": "规则版本号"
    }
  }
}'''

RELATION_SCHEMA_JSON = '''{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KnowledgeRelation",
  "description": "知识卡片间的轻量关系模型 - 六类关系定义",
  "type": "object",
  "required": ["relation_id","src","rel_type","dst"],
  "properties": {
    "relation_id": {
      "type": "string",
      "pattern": "^REL-[0-9]{4}$",
      "description": "关系唯一标识"
    },
    "src": {
      "type": "string",
      "description": "源卡片ID"
    },
    "rel_type": {
      "type": "string",
      "enum": ["precedes","triggered_by","alternatives","refines","forbids_with","escalates_to"],
      "description": "关系类型（六类之一）"
    },
    "dst": {
      "type": "string",
      "description": "目标卡片ID（或条件ID）"
    },
    "bidirectional": {
      "type": "boolean",
      "default": false,
      "description": "是否双向关系（alternatives和forbids_with默认为true）"
    },
    "condition": {
      "type": "string",
      "description": "关系生效条件（可选），如：当直接加压无效时"
    },
    "weight": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "default": 1.0,
      "description": "关系权重，用于检索扩展时的置信度排序"
    },
    "annotation": {
      "type": "string",
      "description": "关系标注说明，供专家审阅"
    },
    "evidence": {
      "type": "object",
      "properties": {
        "source": {"type": "string"},
        "section": {"type": "string"}
      },
      "description": "关系依据（可选）"
    }
  }
}'''

RELATION_TYPE_DEFINITIONS = [
    ("precedes", "流程编排", "A在处置流程上先于B执行",
     "CARD-HEM-TQ-001 precedes CARD-HEM-WOUND-002",
     "单向", "确定处置顺序，生成多步应答"),
    ("triggered_by", "条件触发", "当条件C满足时，触发执行卡A",
     "COND-ARTERIAL-BLEED triggered_by CARD-HEM-TQ-001",
     "单向", "症状→处置映射，实现条件分支"),
    ("alternatives", "替代路径", "A与B功能等价，可互相替代",
     "CARD-HEM-TQ-001 alternatives CARD-HEM-PRESSURE-003",
     "双向", "资源不可用时自动切换替代方案"),
    ("refines", "细化展开", "A是B的细化子步骤或详细说明",
     "CARD-MARCH-H-OVERVIEW refines CARD-HEM-TQ-001",
     "单向（父→子）", "从总览深入到具体操作"),
    ("forbids_with", "禁忌检测", "A与B不能同时应用于同一伤员",
     "CARD-HEM-TQ-001 forbids_with CARD-HEM-JOINT-TQ",
     "双向", "自动检测处置冲突，触发安全告警"),
    ("escalates_to", "升级指引", "A不奏效或超出能力时升级到B",
     "CARD-HEM-TQ-001 escalates_to CARD-EVAC-URGENT",
     "单向", "失败后的降级/后送/升级路径"),
]
