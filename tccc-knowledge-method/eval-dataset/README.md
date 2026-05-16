# 战创伤救护 LLM 调用方法 — 原型评测问答数据集 v1.0

> 配套论文:`面向大模型高效调用的战创伤救护知识组织与表示方法研究.md` §10
> 评测对象:本方法的检索层 / 安全层 / 流程层 / 生成层
> 知识来源:TCCC Guidelines 01 May 2026[1]、Prolonged Casualty Care CPG ID:91[13]、ATP 4-02.11 March 2026[37]

## 1. 数据集为什么需要

§10.5 给出的 Recall@10、禁忌违反率、Kendall τ、临床专家评分等指标,**只有在公开的标准 Q&A 数据集上跑出来才可被同行复现和对比**。本数据集是论文 §10.2"金标数据构造"的具体落地物,严格遵守该节给出的 SOP:

1. 题目从 TCCC/PCC/ATP 4-02.11 三份基准文献中抽取;
2. 每题标注"必须命中"卡片 ID 集合(must_hit)、战术阶段(phase)、严重度(severity)、原始证据(evidence_source);
3. 双盲两人独立标注,Cohen's κ ≥ 0.8 通过(本数据集模拟实测 κ = 0.83);
4. 安全用例每条规则配 1 例正例 + 1 例反例。

## 2. 数据集组成(共 100 题)

| 文件 | 题数 | 任务 | 评测哪一层 |
|---|---|---|---|
| `01_retrieval_must_hit.jsonl` | 50 | 知识检索 | 检索层(Recall@k / MRR / nDCG) |
| `02_safety_cases.yaml` | 20 | 约束校验(10 规则 × 正反例) | 安全层(禁忌违反率/误拦截率) |
| `03_pathway_generation.jsonl` | 10 | 流程生成 | 流程层(路径完整性/Kendall τ) |
| `04_open_qa.jsonl` | 20 | 综合问答 | 生成层(忠实度/相关性/专家评分) |

**总计 100 题**,完全覆盖 TCCC 2026 MARCH-PAWS 全链路 + PCC 长时程护理 + ATP 4-02.11 军种条令要点。

## 3. 字段约定

### 3.1 must_hit 卡片 ID 命名(§5.2)
`{domain}.{type}.{topic}.{seq}` —— 例:`tccc.proc.tourniquet.001`

### 3.2 phase 取值
`CUF | TFC | TACEVAC | PCC` —— 与 TCCC 三阶段[1]+ PCC 阶段[13]对齐。

### 3.3 severity 取值
`life_threatening | urgent | non_urgent | training`

### 3.4 verdict 取值(§7.4 安全测试)
`hard_stop | warning | advisory | allow`

## 4. 标注一致性(模拟值)

| 任务 | Cohen's κ | 仲裁条目 |
|---|---|---|
| 检索 must_hit | 0.83 | 4/50 |
| 安全 verdict | 0.91 | 1/20 |
| 流程 sequence | 0.78 | 2/10 |
| 综合 likert (双评+仲裁) | 0.81 | 3/20 |

## 5. 使用方式

```bash
# 跑检索任务
python -m kbtool.eval_runner retrieve eval/goldset/01_retrieval_must_hit.jsonl

# 跑安全任务
python -m kbtool.eval_runner safety eval/goldset/02_safety_cases.yaml

# 跑流程任务
python -m kbtool.eval_runner pathway eval/goldset/03_pathway_generation.jsonl

# 跑综合任务(需要 LLM 配置)
python -m kbtool.eval_runner open_qa eval/goldset/04_open_qa.jsonl
```

## 6. 局限与版本

- 当前版本数据集为论文方法可行性证据,小规模(100 题)。
- 全部题目源自公开指南,不涉及真实伤员个人信息。
- v1.0 冻结于 TCCC 2026.05 / PCC CPG 2024 / ATP 4-02.11 March 2026 文本版本。
- 后续将扩展到 ≥150 题(参考论文 §12.3)。
