# LLM 抽取 × 机理校验：机理-数据融合的创伤失血性休克（THS）数字孪生方案

> 本文系本仓库 [`机理-数据驱动数字孪生论文分类与创伤失血性休克适用性分析.md`](./机理-数据驱动数字孪生论文分类与创伤失血性休克适用性分析.md)、[`从原始电子病历到结构化JSON与自然语言叙事配对.md`](./从原始电子病历到结构化JSON与自然语言叙事配对.md) 与原型实现 [`创伤失血性休克数字孪生原型/`](./创伤失血性休克数字孪生原型/) 的延伸。
> 重点回答：**能否用深度学习 / 大语言模型（LLM、VLM）对临床电子病历的图像与文本进行自动抽取与模型生成，并由机理模型对其进行校验或约束**；并在此基础上给出 **可工程实现的 THS 机理-数据融合数字孪生最小原型设计**。

---

## 0. 一句话结论（TL;DR）

- **可行**，但应将"LLM/VLM 抽取"与"机理孪生"放在 **双向闭环** 里，而不是把 LLM 当成"端到端预测器"：
  - **LLM/VLM → 机理孪生**：负责把抢救记录、检验报告、监护波形截图、影像报告等 **多模态非结构化 EMR**，抽取为机理模型可消费的 **结构化时间序列 + 干预事件 + 不确定性**；
  - **机理孪生 → LLM/VLM**：用 0D/低阶生理模型 + UKF 对抽取结果做 **物理一致性校验、缺失插补、矛盾标记**，并把不一致项以 critique 形式回写给 LLM 进行复抽取。
- **机理模型不是 LLM 的替代品，而是 LLM 在 ICU/急救场景下的"硬约束守门员"**：质量、能量、压力-流量等守恒律，以及生理可行域（HR ∈ [20,220]、MAP ∈ [20,180]、Hb ∈ [20,200] g/L 等），都是不可被 LLM 逻辑覆盖的"先验真值"。
- 现有证据足以支撑该思路：LLM 用 EHR 自由文本预测多变量轨迹（DT-GPT，npj Digital Medicine, 2025）；LLM 用作临床试验数字孪生（TWIN-GPT，arXiv 2404.01273）；VLM 在急救/重症诊断已有基准（Nature 子刊 2025 PMC12246445）；物理-信息神经网络/算子在血流动力学参数估计上达成实时化（PINODE、PIONet 2025）。同时医学 LLM 的幻觉率仍可达 30–60%（PMC41610815、2503.05777），必须有外部约束层。

---

## 1. 问题陈述与可行性命题

### 1.1 在 THS 场景下的真实数据形态

院前 + 急诊 + ICU 全链路下的 EMR 是 **强多模态、强异步、低采样、高缺失** 的：

| 模态 | 例子 | LLM/VLM 直接消费难度 | 机理模型需要的字段 |
| --- | --- | --- | --- |
| 自由文本 | 抢救记录、入院记录、手术记录 | 低（文本 LLM 强项） | 失血量估计、休克分级、手术时间轴 |
| 半结构化表 | 体温单、出入量、用药单 | 中（需 schema 对齐） | 输液速率、血制品速率、血管活性药剂量 |
| 高频时序 | 监护仪 HR/SpO₂/IBP/CVP、呼吸机波形 | 中（多采样率/丢点） | 状态观测 y(t)，UKF 输入 |
| 检验/血气 | Hb、Lac、BE、Hct、TEG/ROTEM | 中（单位/参考区间） | 失血严重度、凝血状态 |
| 图像 | 床旁超声 FAST、CT、X 光 | 高（需 VLM/专科模型） | 出血部位/体腔积血/血肿 |
| 监护截图 | 厂商导出 PNG、护士手抄 | 高（OCR + 表格还原） | 关键事件时间戳 |
| 语音 | 抢救口头医嘱 | 中（ASR + LLM） | 干预事件流 u(t) |

**核心命题**：单纯让 LLM "看完所有 EMR 直接预测患者轨迹"会触发三类不可接受的失败——幻觉、违反守恒律、外推到未见过的干预空间。引入 0D 心血管-血容量-氧输送机理模型作为"代价函数 + 可行域过滤器"，可以把这些失败转化为可检测、可拒绝的事件。

### 1.2 可行性命题（要在原型中被证伪/证实）

- **C1（抽取可行性）**：在 ≤7B 参数级别的开源 LLM + 轻量 VLM 上，对中文抢救记录的关键字段抽取（失血量、补液、用血、血管活性药、关键时点）F1 可达 ≥0.80。
- **C2（机理校验有效性）**：把 LLM 抽取结果送入 0D 模型 + UKF 后，**物理不一致样本**（如"输入 6 单位红细胞却 Hb 反而下降 30 g/L 且无再出血记录"）能被自动标红，召回率 ≥0.9。
- **C3（双向闭环增益）**："LLM 抽取 → 机理校验 → critique 回写 → LLM 复抽取"两轮，相对单轮直接抽取，关键字段错误率下降 ≥30%。
- **C4（孪生预测增益）**：以校验后参数化的 0D 模型预测未来 30 min MAP、HR、Hb 轨迹的 MAE，相对纯 LLM(DT-GPT 风格) 与纯机理（固定参数）双基线均显著降低。

C1–C4 即原型的验收指标（见 §6.4）。

---

## 2. 文献证据：本仓库 mechic-data-driven 内 + 外部最新支撑

### 2.1 本仓库 [`机理-数据驱动数字孪生论文分类...md`](./机理-数据驱动数字孪生论文分类与创伤失血性休克适用性分析.md) 中已隐含支持的方向

按其分类法：

- **A 类（机理为骨、数据为肉）**：UKF/EKF/MCMC 做参数辨识、PINN 嵌入 ODE 残差。这是 LLM 抽取层下游天然的"承接者"——LLM 给出 y(t) 与 u(t)，A 类方法把它们变成 θ̂(t)。
- **B 类（数据为骨、机理为约束）**：物理-信息损失、可行域投影、Lagrange 罚。这正是用来约束 LLM 输出的工具——把"LLM 抽取的 Hb 必须满足 dHb/dt ≈ -失血率/血容量"写成软/硬约束。
- **C 类（机理-数据并行融合）**：孪生 + 实时数据同化、闭环控制。THS 抢救本身是闭环（输液-MAP-Hb 反馈），LLM 在此扮演"事件流解析器"。

> 因此 mechic-data-driven 仓库内的论文虽未直接讨论 LLM，但其"机理-数据接口"恰好就是 LLM 抽取后需要的接口，**等价于给 LLM 留好了下游插槽**。

### 2.2 外部最新支撑工作（2024–2026）

> 以下信息均经过改写以满足来源合规要求；详细论点请回到原文。Content was rephrased for compliance with licensing restrictions.

| # | 工作 | 与本方案的对应位置 | 关键启示 |
| --- | --- | --- | --- |
| L1 | DT-GPT — [Nature npj Digital Medicine 2025](https://www.nature.com/articles/s41746-025-02004-3)、[medRxiv preprint](https://www.medrxiv.org/content/10.1101/2024.07.05.24309957v2.full.pdf+html) | 抽取 + 预测层 | 用 EHR 文本叙事直接驱动 LLM 做多变量轨迹预测，不需要补缺/标准化，验证了"EHR-as-text"路径 |
| L2 | TWIN-GPT — [arXiv 2404.01273](https://arxiv.org/abs/2404.01273) | 个体化数字孪生层 | LLM 在小样本下也能跨数据集合成"可个体化"的临床试验孪生；适合 THS 这种小样本高异质场景 |
| L3 | AgentClinic — [Nature 子刊 2026](https://www.nature.com/articles/s41746-026-02674-7)、[arXiv 2405.07960](https://arxiv.org/abs/2405.07960) | LLM-Agent 工具调用 | 临床决策需要序贯+多模态+工具调用，单回合 QA 不足以反映真实场景；支持把 0D 模型作为 LLM 的 tool |
| L4 | CDR-Agent — [ResearchGate 2025](https://www.researchgate.net/publication/392204377) | 决策规则选择 | LLM 自动从非结构化笔记选择并执行临床决策规则，适合急诊分诊与抢救流程模板匹配 |
| L5 | EHR-MCP — [arXiv 2509.15957](https://arxiv.org/abs/2509.15957) | 安全数据访问 | Model Context Protocol 让 LLM 在医院环境下走"工具化"读 EHR，简单任务接近完美；复杂任务仍需校验层 |
| L6 | FeatEHR-LLM — [arXiv 2604.22534](https://arxiv.org/abs/2604.22534) | 隐私安全 | LLM 仅看 schema/任务描述生成特征，不直接看患者原始记录；为本方案 §7.3 隐私层提供模板 |
| L7 | 急救/ICU VLM 基准 — [Nature 子刊 PMC12246445](https://pmc.ncbi.nlm.nih.gov/articles/PMC12246445/) | 影像/截图层 | 现成 VLM 在急救与重症诊断任务上已有评估方法和阈值，可直接复用 |
| L8 | 物理-信息血流动力学算子学习 — [arXiv 2509.17293](https://arxiv.org/abs/2509.17293)、[Int J Numer Method Biomed Eng PMC12905477](https://pmc.ncbi.nlm.nih.gov/articles/PMC12905477/) | 机理代理模型层 | PINN/算子学习把 0D/1D 心血管模型加速到实时，可直接服务于床旁推理 |
| L9 | PINODE — [Sci Rep PMC10287651](https://pmc.ncbi.nlm.nih.gov/articles/PMC10287651/) | 物理嵌入 | 把 ODE 当 collocation 嵌入神经 ODE，给"LLM 抽取参数 → 机理预测"提供平滑可微的软约束实现 |
| L10 | PIML 综述 — [arXiv 2510.05433](https://arxiv.org/html/2510.05433) | 总体范式 | 物理-信息 ML 在生物医学的现状、风险、评估指标，可直接套用到 THS |
| L11 | 医学幻觉评估 — [arXiv 2503.05777](https://arxiv.org/abs/2503.05777)、[arXiv 2412.18947](https://arxiv.org/html/2412.18947v2) | 失败模式分析 | 给出医学幻觉的工程定义与基准；说明 **必须** 加约束层 |
| L12 | 本体接地 KG 抑制幻觉 — [PubMed 41610815](https://pubmed.ncbi.nlm.nih.gov/41610815/) | 校验层模板 | 本体 + KG 把 ChatGPT-4 / DeepSeek-R1 的幻觉率从 ~63% / ~48% 降到 ~1.7%，证明"外部知识硬约束"路径有效 |
| L13 | LLM 生成 EHR 表型算法 — [PMC10775330](https://pmc.ncbi.nlm.nih.gov/articles/PMC10775330/) | 自动化抽取规则 | 用 LLM 自动写 phenotyping 规则，减少人工 schema 维护成本 |
| L14 | CELEC — [arXiv 2511.00772](https://arxiv.org/html/2511.00772v2) | NL→SQL | 医院环境下用受控 NL→SQL 取数，给本方案 §3.4"安全数据网关"提供可借用的 prompting 范式 |
| L15 | ICU AI 监管综述 — [Nature 子刊 2026](https://www.nature.com/articles/s41746-026-02535-3) | 合规层 | 从"窄模型"到"通用 LLM/Agent"的监管演变，本方案的安全联锁需要直面这条曲线 |
| L16 | 创伤脑损伤报告生成 — [arXiv 2510.08498](https://arxiv.org/html/2510.08498v1) | 影像报告 | 多尺度特征 + Transformer 用于颅内出血等创伤影像报告，THS 中颅外出血场景同构 |
| L17 | 农村/MCI 合成 EHR — [arXiv 2605.09951](https://arxiv.org/html/2605.09951v1) | 数据增强 | 用 agent-based 模型生成大批量 MCI 场景 EHR，弥补 THS 真实数据稀缺 |
| L18 | AIPatient — [arXiv 2409.18924](https://arxiv.org/abs/2409.18924) | 仿真患者 | RAG + 知识图谱构建仿真患者，可作为 §6 闭环测试的"合成患者发生器" |

> 综合 L1–L18：**"LLM/VLM 抽取 EMR + 机理模型校验/约束"既不是空想，也不是单点工作的简单拼装，而是 2024–2026 年医学 AI 的明确收敛方向**——但所有现成工作都缺少"机理硬约束层"或"急救场景全链路闭环"，正是本仓库 THS 数字孪生原型的差异化贡献空间。

### 2.3 风险证据

- 通用 LLM 在医学事实上的幻觉率仍偏高（L11、L12）。
- 生物医学专用 LLM 在未见数据上不一定优于通用模型 [arXiv 2408.13833](https://arxiv.org/html/2408.13833v1)。
- VLM 在低资源语言或非英文报告上性能下降 [arXiv 2505.01096](https://arxiv.org/html/2505.01096v1)。
- 监管侧对生成式/agent 系统在 ICU 内的部署仍处于早期（L15）。

→ 这三类风险**直接决定了本方案必须以"机理 = 守门员、LLM = 解析+建议"为基础架构**，而不是"LLM = 主决策器"。

---

## 3. 总体方案：LLM-extract × 机理-validate 双向闭环

### 3.1 核心设计原则

1. **机理优先（Mechanism-first）**：所有 LLM 输出，必须能够在 0D 心血管-血容量-氧输送-凝血模型上"跑得通"。跑不通的，先标可疑。
2. **可拒绝（Reject-able）**：LLM 输出必须可被机理层、规则层、人类层任一拒绝；拒绝路径必须在产品中显式存在。
3. **可解释（Auditable）**：每一条数字孪生状态变量在每一时刻都能回答两个问题：(a) 来自哪条 EMR？(b) 经过哪一次机理校验？
4. **最小信任域（Least-trust LLM）**：LLM 仅做"非结构化 → 结构化"的解析与"复杂语义 → 简单规则"的中介；定量预测交给机理模型 + 数据驱动代理模型。
5. **隐私最小化**：参考 L6，LLM 仅在必要时看到去标识化最少字段；schema/任务描述能完成的工作，不发原始记录。

### 3.2 端到端架构

```
                   ┌─────────────────────────────────────────────────────────┐
                   │                    多模态 EMR 源                         │
                   │ 文本 / 表格 / 监护波形 / 检验 / 影像 / 监护截图 / 语音    │
                   └───────────────┬─────────────────────────────────────────┘
                                   │
                ┌──────────────────▼──────────────────┐
                │  ① 多模态解析层 (LLM / VLM / ASR)     │
                │   - 文本 LLM（中文医疗指令微调）      │
                │   - VLM（监护截图/影像报告）          │
                │   - OCR（手抄单/扫描件）              │
                │   - ASR（口头医嘱）                   │
                └──────────────────┬──────────────────┘
                                   │ 候选 JSON (含字段级置信度)
                ┌──────────────────▼──────────────────┐
                │  ② 本体 / 规则校验层                  │
                │   - 单位、参考区间、UMLS/ICD/LOINC   │
                │   - 时间序与因果序                    │
                │   - 互斥/共现规则                     │
                └──────────────────┬──────────────────┘
                                   │ 通过的 JSON + 可疑标记
        ┌──────────────────────────▼──────────────────────────┐
        │  ③ 机理孪生层（复用现有 ths_dt 原型）                 │
        │   - 0D 心血管 / 血容量 / 氧输送 / 凝血                │
        │   - UKF 状态-参数联合估计                             │
        │   - 复用 model.py / simulator.py / ukf.py             │
        └──────┬───────────────────────────────┬───────────────┘
               │ 物理一致性                     │ 状态/参数估计
               │                                │
        ┌──────▼─────────────────┐      ┌──────▼─────────────────┐
        │ ④ critique 生成器       │      │ ⑤ 闭环决策 / 控制建议   │
        │   - 残差 > 阈值 ⇒ 反馈   │      │   - 复用 controller.py  │
        │   - 自然语言 critique    │      │   - 输液/血管活性药速率 │
        │   - JSON-Patch 候选     │      │   - 安全联锁 + 人审      │
        └──────┬─────────────────┘      └──────┬─────────────────┘
               │                                │
               │           ┌────────────────────┘
               │           │
        ┌──────▼───────────▼─────┐
        │ ⑥ LLM/VLM 复抽取（Round 2）│  ⇆  ⑦ 工具化数据网关 (MCP / NL→SQL)
        └────────────────────────┘
                  │
                  ▼
            最终冻结 JSON + 可视化 + 审计链
```

### 3.3 各模块职责

| 模块 | 输入 | 输出 | 失败模式 | 兜底 |
| --- | --- | --- | --- | --- |
| ① 解析 | 多模态 EMR | 字段级 JSON + 置信度 | 幻觉、单位错、漏字段 | 置信度阈值 + ② 校验 |
| ② 本体校验 | ① 的 JSON | 通过 + 标记 | 本体未覆盖 | 转人工或下推到 ③ |
| ③ 机理孪生 | ② 的时序 | 状态/参数估计 + 残差 | 模型欠拟合 / 不可观 | 提高过程噪声、退化为统计基线 |
| ④ critique | ③ 的残差 | NL critique + JSON-Patch | 假阳性 critique | 至多两轮，强制人审 |
| ⑤ 决策 | ③ 的状态/参数 | 干预建议 | 模型外推 | 安全联锁，仅建议 |
| ⑥ 复抽取 | ① 原文 + ④ critique | 修正 JSON | 与 ④ 冲突 | 人审仲裁 |
| ⑦ 数据网关 | LLM 工具调用 | 受限 SQL/字段 | 越权 | RBAC + 审计日志 |

### 3.4 关键接口约定（最小必要 schema）

```jsonc
// extraction_v0.json（②校验后冻结，③直接消费）
{
  "patient_id": "P001",                 // 去标识化伪 ID
  "t0_iso": "2026-05-25T10:00:00+08:00",
  "events": [                           // 干预 u(t)，按时间升序
    { "t_min": 0,   "type": "fluid_crystalloid", "rate_ml_min": 50 },
    { "t_min": 5,   "type": "fluid_blood_prbc",  "units": 2 },
    { "t_min": 8,   "type": "vasopressor_norepi", "ug_kg_min": 0.1 },
    { "t_min": 15,  "type": "hemorrhage_control", "method": "tourniquet" }
  ],
  "observations": [                     // 观测 y(t)
    { "t_min": 0,  "hr_bpm": 130, "map_mmhg": 55, "spo2": 0.94, "hb_g_l": 95 },
    { "t_min": 10, "hr_bpm": 120, "map_mmhg": 65, "spo2": 0.96, "hb_g_l": 88 }
  ],
  "confidence": {                       // 字段级置信度
    "events[1].units": 0.78,
    "observations[1].hb_g_l": 0.92
  },
  "provenance": {                       // 审计链
    "events[0]": "rescue_note.txt#L12",
    "observations[0]": "monitor_export.csv#row=23"
  }
}
```

---

## 4. 分阶段技术方案（每阶段补充完整）

> 每阶段给出：**目标、输入/输出、技术选型、关键算法/Prompt、验收指标、回退策略**。

### 阶段 0：数据准备与去标识化

- **目标**：建立"原始 EMR → 训练/评估子集"的可重复管道，满足隐私最小化。
- **输入**：医院 HIS/PACS/监护中心导出的多模态原始记录。
- **输出**：去标识化的 jsonl + 多模态附件 + schema。
- **技术选型**：
  - 文本去标识：基于 [Presidio](https://github.com/microsoft/presidio) + 中文规则字典。
  - 影像去标识：DICOM 标签洗白（pydicom + dcmqi）+ 像素级 burnt-in PHI 抹除。
  - 监护波形：保留时间轴相对偏移，丢弃绝对日期。
- **关键算法**：
  - 字段最少必要：默认仅保留 §3.4 schema 中列出的字段。
  - 时间轴相对化：所有 `t_min` 相对于"急诊登记"。
- **验收指标**：随机抽 50 条人工复核，PHI 残留 = 0；LLM 在去标识数据上的抽取性能与原始数据差距 < 5%。
- **回退**：若去标识工具误删关键字段，加白名单（如"血压"误判为电话号码时）。

### 阶段 1：多模态解析层（LLM / VLM / OCR / ASR）

- **目标**：把异构 EMR 解析为 §3.4 的候选 JSON。
- **技术选型**：
  - 文本 LLM：中文 7B 级开源（Qwen2.5-7B-Instruct / GLM-4-9B / DeepSeek-V2-Lite）+ LoRA 医疗指令微调。
  - VLM：Qwen2.5-VL-7B 或 InternVL2-8B；急救/重症任务可参考 L7 基准。
  - OCR：PaddleOCR + 表格还原（[PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)）。
  - ASR：FunASR / Whisper-large-v3-turbo（中文医疗词典热词）。
- **关键 Prompt（节选，文本 LLM）**：

```
你是创伤抢救 EMR 抽取助手。请仅依据[输入]中的字面信息，输出严格符合
[schema] 的 JSON。禁止凭常识补全；不确定字段填 null 并在 confidence
中给出 0~1 的实数。涉及单位时严格使用 schema 单位（mmHg/g·L⁻¹/mL·min⁻¹
等）。同一事件重复记录时按时间最早一次为准。

[schema]
{...§3.4 的 JSON Schema...}

[输入]
{抢救记录文本，含[t=...]时间戳的口头医嘱}
```

- **多模态融合策略**：
  - **晚融合（推荐）**：每模态独立解析为局部 JSON，再由"合并 Agent"按 patient_id + t_min 取并集，冲突进入 ② 层裁决。
  - **早融合（消融）**：VLM 直接看监护截图 + 文本上下文，作为基线对比。
- **验收指标**：随机 200 例的字段级 F1：
  - 数值字段（HR/MAP/Hb/Lac）F1 ≥ 0.85；
  - 事件字段（输液/输血/血管活性药）F1 ≥ 0.80；
  - 时间戳误差 ≤ 1 min 占比 ≥ 0.85。
- **回退**：当 LLM 自报置信度 < 0.5 或 schema 解析失败时，路由到规则模板（正则 + 词典）兜底。

### 阶段 2：本体 / 规则校验层

- **目标**：在不调用机理模型前，用 **便宜且确定** 的规则先把"低级错误"挡住。
- **校验类别**：
  1. **单位与量纲**：mmHg vs kPa、g/L vs g/dL；统一到 SI。
  2. **生理可行域**：见 §3.1 表（HR/MAP/Hb/SpO₂ 范围）。
  3. **本体接地**：药品 → ATC 编码；检验 → LOINC；诊断 → ICD-10。参考 L12 的本体-KG 校验范式。
  4. **时间序与因果序**：tourniquet 必须先于解除时间；血制品输注开始 < 结束；插管时间 < 拔管时间。
  5. **互斥/共现**：同一时刻不能同时存在"已死亡"与新观测；血气与中心静脉血气来源标记必须存在。
- **实现**：JSON Schema + [Pydantic v2](https://docs.pydantic.dev/) 自定义校验器；本体查询用本地缓存 + 离线 RxNorm/LOINC 子集。
- **验收指标**：人工注入 100 条已知错误，召回 ≥ 0.95、误报 ≤ 0.10。
- **回退**：未通过项不丢弃，标记 `flagged=true` 后仍送入 ③，让机理层再判一次。

### 阶段 3：机理孪生层（直接复用现有原型）

- **目标**：用 0D 心血管-血容量-氧输送(-凝血) 模型 + UKF 做联合状态/参数估计，并产出残差。
- **复用**：
  - [`ths_dt/model.py`](./创伤失血性休克数字孪生原型/ths_dt/model.py)：心输出量、外周阻力、血容量、氧输送等状态方程。
  - [`ths_dt/simulator.py`](./创伤失血性休克数字孪生原型/ths_dt/simulator.py)：RK4/SciPy 推进。
  - [`ths_dt/ukf.py`](./创伤失血性休克数字孪生原型/ths_dt/ukf.py)：UKF 同化。
  - [`ths_dt/controller.py`](./创伤失血性休克数字孪生原型/ths_dt/controller.py)：闭环干预建议。
- **新增**：
  - **抽取适配器** `extraction_to_ukf.py`：把 §3.4 的 JSON 转成 UKF 的 `(t, y, u)` 序列；缺失字段以 NaN 进入观测协方差膨胀。
  - **凝血子模块**（可选）：纤维蛋白/血小板二阶动力学，对应 TEG/ROTEM 解析字段。
- **关键算法**：
  - **观测协方差自适应**：用 LLM 给的 `confidence[field]` 反比例地放大对应观测噪声 R(t)。
  - **过程噪声分配**：失血率、外周阻力、毛细血管渗漏率作为可时变参数 θ(t)，用 random walk 模型嵌入 UKF 增广状态。
  - **外推闭锁**：当 UKF 后验协方差突破阈值或残差白噪声检验失败，进入"仅观测、不预测"安全模式。
- **验收指标**：
  - 在合成数据上：θ̂ 相对真值 RMSE ≤ 15%。
  - 在真实数据上：对未来 15/30 min MAP/HR 的 MAE 相对 ARIMA 基线下降 ≥ 20%。
- **回退**：当模型残差长期不可白化，自动切换到"统计代理模型"（L8 风格 PINN 算子）作为短期基线。

### 阶段 4：双向校验 — 机理 critique 反馈给 LLM

- **目标**：把机理层的物理不一致转成自然语言 critique，回到阶段 1 形成 Round 2 抽取。
- **触发条件**：
  - 守恒律违反：`d(Hb·V_blood)/dt + 失血贡献 ≠ 输血贡献`，残差 > 阈值。
  - 干预-效应不一致：6 单位红细胞已输注 ≥ 30 min，但 Hb 反向下降，且无再出血或稀释解释。
  - 观测自洽性：HR↑↑ 但 MAP 同向↑↑ 且无去甲肾上腺素加量，物理上罕见。
- **critique 模板**：

```
[Critique to extractor]
- field: events[1].units
- observed: 2 units PRBC at t=5min
- mechanism check failed: predicted ΔHb = +14 g/L over 20min,
  measured ΔHb = -7 g/L; no documented re-bleed or dilution event.
- candidate fixes (rank by likelihood):
  1) units 应为 1（请重读病历"2U"是否为"1U"误录）
  2) 时间戳 t=5min 应为 t=15min（请检查口头医嘱时序）
  3) 在 t∈[5,25]min 区间内可能漏抽取一次再出血事件
请基于原始 EMR 重新抽取受影响字段，并保持其余字段不变。
```

- **JSON-Patch 候选**：critique 同时提供 [RFC 6902](https://datatracker.ietf.org/doc/html/rfc6902) 形式的 patch，方便 LLM 选择性接受。
- **收敛策略**：最多 2 轮迭代；仍未通过则标记 `requires_human_review=true`，进入工单。
- **验收指标**：注入合成错误后，关键字段错误率两轮内下降 ≥ 30%（C3）。

### 阶段 5：闭环决策与控制建议

- **目标**：在校验通过的孪生上，给出**建议性**干预动作，绝不自动执行。
- **复用**：[`controller.py`](./创伤失血性休克数字孪生原型/ths_dt/controller.py)（可基于 MPC 或规则）。
- **安全联锁**：
  - 仅在 UKF 后验协方差 < 阈值 时启用建议；
  - 输液速率、血制品速率、血管活性药剂量均 clip 到指南上下限（如 EAST/STOP THE BLEED 指南）；
  - 任何超出训练-验证分布的建议，自动降级为"提示风险"而非"建议数值"。
- **可解释报告**：每条建议附"基于 …小时内 Hb 趋势 + …mL 失血估计 + 当前 MAP… → 建议输液 …mL/min，置信区间 …"。

### 阶段 6：不确定性量化与安全联锁

- **三类不确定性**：
  - LLM/VLM 抽取不确定性（field-level confidence）；
  - 机理模型结构不确定性（残差白噪声检验）；
  - 参数后验不确定性（UKF Pₖ）。
- **聚合为风险标签**：`green / yellow / red`，影响是否启用决策建议。
- **看板**：与原型 `examples/run_demo.py` 的可视化合并，新增 `confidence ribbon`。

### 阶段 7：验证、监管、伦理

- **验证层**：
  - **单元层**：每个模块 ≥ 80% 行覆盖；机理模型用方法学测试（守恒律、稳态点）。
  - **场景层**：以 L17 风格生成 MCI 合成数据 + 来自 MIMIC-IV / eICU 的真实 ICU 子集做回归。
  - **临床层**：与本院创伤团队做"影子模式"评估（仅展示，不干预），≥ 200 例。
- **监管层**：
  - 参照 L15，把 LLM/Agent 与机理孪生 **分别** 走 SaMD 风险等级评估；
  - 模型卡（model card）+ 数据卡（data card）+ 风险登记册必备。
- **伦理层**：
  - 默认 opt-in；
  - 保留人工最终决策权；
  - 公平性审计：按性别、年龄段、损伤机制分层评估抽取与预测性能。

---

## 5. 与已有原型的衔接

现有原型 [`创伤失血性休克数字孪生原型/`](./创伤失血性休克数字孪生原型/) 已提供阶段 3、阶段 5 的最小骨架。本方案要求在其上 **只增不改**：

```
创伤失血性休克数字孪生原型/
├── ths_dt/
│   ├── model.py          # 复用
│   ├── simulator.py      # 复用
│   ├── ukf.py            # 复用
│   ├── controller.py     # 复用
│   ├── extraction_io.py  # 新增：JSON ↔ (t,y,u) 适配器
│   ├── ontology.py       # 新增：阶段 ② 校验
│   ├── critique.py       # 新增：阶段 ④ critique 生成
│   └── llm_client.py     # 新增：阶段 ① / ⑥ 的统一 LLM 接口
├── prompts/              # 新增：所有 prompt / schema
│   ├── extract_text.tmpl
│   ├── extract_vlm.tmpl
│   └── extraction_v0.schema.json
├── data/
│   ├── synthetic/        # 合成 EMR (供单元/场景测试)
│   └── shadow/           # 真实影子模式数据 (受控)
├── examples/
│   ├── run_demo.py            # 现有
│   ├── run_cohort.py          # 现有
│   └── run_llm_loop_demo.py   # 新增：端到端闭环 demo
└── tests/
    ├── test_model.py     # 现有
    ├── test_extraction.py
    ├── test_ontology.py
    ├── test_critique.py
    └── test_loop.py
```

---

## 6. 最小化原型设计（端到端跑通）

> 目标：**在一周以内** 跑通"合成 EMR → LLM 抽取 → 本体校验 → 0D + UKF → critique → Round-2 抽取 → 决策建议"完整链路，并产出一个可演示脚本。

### 6.1 范围与依赖

- **范围**：
  - 单患者、单事件流；
  - 文本模态优先，VLM/ASR 列为可选项；
  - 0D 模型采用现有 `model.py` 简化版（心血管 + 血容量 + 氧输送，凝血先桩化）。
- **依赖**：
  - Python 3.11；
  - `numpy`, `scipy`, `pydantic>=2`, `jsonpatch`, `matplotlib`, `pandas`；
  - LLM：本地用 [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) 跑 Qwen2.5-7B-Instruct GGUF；线上可走 OpenAI 兼容 API，由 `llm_client.py` 抽象。

### 6.2 端到端 demo 控制流（伪代码）

```python
# examples/run_llm_loop_demo.py
from ths_dt.llm_client import LLM
from ths_dt.ontology import validate_extraction
from ths_dt.extraction_io import to_ukf_inputs
from ths_dt.simulator import Simulator
from ths_dt.ukf import THS_UKF
from ths_dt.critique import build_critique
from ths_dt.controller import suggest_intervention

raw = open("data/synthetic/case_001.txt").read()
schema = open("prompts/extraction_v0.schema.json").read()

llm = LLM(model="qwen2.5-7b-instruct", schema=schema)

extraction = llm.extract(raw, prompt="prompts/extract_text.tmpl")  # round 1

for round_id in range(2):
    issues = validate_extraction(extraction)               # 阶段 ②
    t, y, u, R = to_ukf_inputs(extraction)                 # 阶段 ③ 入口
    ukf = THS_UKF()
    states, params, residuals = ukf.run(t, y, u, R)
    critique, patches = build_critique(extraction, residuals, issues)  # ④
    if not critique:
        break
    extraction = llm.repair(raw, extraction, critique, patches)        # ⑥

suggestion = suggest_intervention(states[-1], params[-1])               # ⑤
print({"final": extraction, "suggestion": suggestion,
       "uncertainty": float(residuals.std())})
```

### 6.3 关键模块骨架

```python
# ths_dt/extraction_io.py（节选）
import numpy as np

def to_ukf_inputs(extraction: dict):
    obs = extraction["observations"]
    evs = extraction["events"]
    t = np.array([o["t_min"] for o in obs], dtype=float)
    y = np.array([[o.get("hr_bpm", np.nan),
                   o.get("map_mmhg", np.nan),
                   o.get("spo2", np.nan),
                   o.get("hb_g_l", np.nan)] for o in obs], dtype=float)
    # 字段级置信度 → 观测噪声 R 的对角块；置信度低 → 噪声大
    conf = extraction.get("confidence", {})
    R = np.eye(y.shape[1])
    base = np.array([4.0, 4.0, 0.01**2, 4.0])  # σ²
    R = np.diag(base.copy())
    # 干预 u(t)：把 events 离散化到 1-min 网格
    T = int(t.max()) + 1
    u = np.zeros((T, 4))   # [crystalloid_ml_min, prbc_ml_min, norepi_ug_kg_min, hemo_ctrl]
    for e in evs:
        ti = int(e["t_min"])
        if e["type"] == "fluid_crystalloid":
            u[ti:, 0] = e["rate_ml_min"]
        elif e["type"] == "fluid_blood_prbc":
            u[ti:ti+30, 1] += e["units"] * 300 / 30  # 300 mL / 30 min
        elif e["type"] == "vasopressor_norepi":
            u[ti:, 2] = e["ug_kg_min"]
        elif e["type"] == "hemorrhage_control":
            u[ti:, 3] = 1.0
    return t, y, u, R
```

```python
# ths_dt/critique.py（节选）
def build_critique(extraction, residuals, issues):
    crits, patches = [], []
    # 1) 物理一致性：Hb 守恒
    hb_residual = residuals.get("hb_conservation", 0.0)
    if abs(hb_residual) > 8.0:   # g/L
        crits.append({
            "field": "events[?].units|observations[?].hb_g_l",
            "reason": f"Hb 守恒残差 {hb_residual:+.1f} g/L 超阈，"
                      "请核对输血单位数或 Hb 时间戳。",
        })
    # 2) 本体/规则层未通过项
    for it in issues:
        crits.append(it)
    return crits, patches
```

```python
# ths_dt/llm_client.py（节选；离线降级到模板）
class LLM:
    def __init__(self, model, schema): ...
    def extract(self, raw_text, prompt):
        # 真实实现走本地 GGUF 或 OpenAI 兼容 API；
        # 离线/CI 跑时返回基于正则的兜底解析。
        ...
    def repair(self, raw_text, prev_extraction, critique, patches):
        ...
```

### 6.4 验收指标（与 §1.2 对应）

| 指标 | 数据 | 目标 | 备注 |
| --- | --- | --- | --- |
| C1 字段级 F1 | 200 例合成 EMR + 50 例真实 | ≥0.80（事件类） / ≥0.85（数值类） | 阶段 1 |
| C2 不一致召回 | 注入 100 条错误 | 召回 ≥0.90，误报 ≤0.10 | 阶段 ②+④ |
| C3 闭环增益 | 同 C1 | 错误率两轮内 ↓ ≥30% | 阶段 ④+⑥ |
| C4 预测 MAE | 真实子集，未来 30 min MAP/HR | 相对 ARIMA / DT-GPT 风格基线显著降低 | 阶段 ③ |

### 6.5 时间线建议

| 周 | 里程碑 |
| --- | --- |
| W1 | 数据合成器 + schema + 文本 LLM 抽取 baseline；C1 初评 |
| W2 | 本体/规则层 + 与现有 0D 模型对接；C2 初评 |
| W3 | critique 闭环 + Round-2 抽取；C3 初评 |
| W4 | UKF 调参 + 决策建议 + 看板；C4 初评 |
| W5 | VLM/OCR 模态 + 影子模式准备 |
| W6 | 真实数据回归 + 模型卡 + 安全审计 |

---

## 7. 局限与风险

1. **真实数据稀缺**：单中心 THS 病例量有限，需要 L17 风格 ABM 合成数据 + 跨中心联邦评估弥补。
2. **凝血/微循环建模不确定性高**：0D 凝血子模块的可辨识性差，UKF 易发散；建议先桩化为分段常数。
3. **LLM 与机理冲突的"谁对"问题**：机理模型本身可能偏（例如对儿童/孕产妇），critique 不应被当作真理；要保留"人审推翻 critique"的路径。
4. **监管路径未定**：参考 L15，agent + 机理混合系统目前在 SaMD 框架下尚无标准评估；建议先以"决策辅助 + 影子模式"形态报批。
5. **隐私与本地化**：原始监护波形与影像不应离开院内；LLM 推理优先选本地化部署或私有云。
6. **评测漂移**：随 LLM 版本迭代，C1–C3 指标会变化，必须建立持续评测流水线。

---

## 8. 与原仓库其他文档的关系

- 本文档 **承接** [`机理-数据驱动数字孪生论文分类与创伤失血性休克适用性分析.md`](./机理-数据驱动数字孪生论文分类与创伤失血性休克适用性分析.md) 的 A/B/C 三类范式：把 LLM/VLM 作为 A 类的"数据前端"、B 类的"软约束伴侣"、C 类的"事件总线"。
- 本文档 **承接** [`从原始电子病历到结构化JSON与自然语言叙事配对.md`](./从原始电子病历到结构化JSON与自然语言叙事配对.md) 的"JSON↔NL"配对：阶段 1 的训练数据，正是该文档输出的一对一配对语料。
- 本文档 **复用并扩展** [`创伤失血性休克数字孪生原型/`](./创伤失血性休克数字孪生原型/) 的 0D 模型、UKF、控制器；新增 4 个模块（`extraction_io.py / ontology.py / critique.py / llm_client.py`）即可形成端到端闭环。

---

## 9. 参考文献（外部支撑工作）

> 引用均经过改写以满足来源合规要求；详细论证请回到原文。Content was rephrased for compliance with licensing restrictions.

- DT-GPT — *Large language models forecast patient health trajectories enabling digital twins*, npj Digital Medicine, 2025. <https://www.nature.com/articles/s41746-025-02004-3>
- TWIN-GPT — *Digital Twins for Clinical Trials via Large Language Model*, arXiv:2404.01273. <https://arxiv.org/abs/2404.01273>
- AgentClinic — *A multimodal benchmark for tool-using clinical AI agents*, npj Digital Medicine, 2026. <https://www.nature.com/articles/s41746-026-02674-7>
- CDR-Agent — *Intelligent Selection and Execution of Clinical Decision Rules Using LLM Agents*, ResearchGate 392204377, 2025.
- EHR-MCP — *Real-world Evaluation of Clinical Information Retrieval by LLMs via Model Context Protocol*, arXiv:2509.15957.
- FeatEHR-LLM — *Leveraging LLMs for Feature Engineering in EHRs*, arXiv:2604.22534.
- *Benchmarking VLMs for diagnostics in emergency and critical care settings*, Nature 子刊, PMC12246445.
- *Physics-Informed Operator Learning for Hemodynamic Modeling*, arXiv:2509.17293.
- *Physics-Informed Emulation of Systemic Circulation*, Int J Numer Method Biomed Eng, 2026, PMC12905477.
- PINODE — *Physics-informed neural ODE*, Sci Rep, PMC10287651.
- *Physics-Informed Machine Learning in Biomedical Science and Engineering*, arXiv:2510.05433.
- *Medical Hallucinations in Foundation Models and Their Impact on Healthcare*, arXiv:2503.05777.
- *A New Benchmark for Assessing Hallucination in Medical LLMs*, arXiv:2412.18947.
- *Ontology-grounded knowledge graphs for mitigating hallucinations in LLMs for clinical QA*, PubMed 41610815.
- *LLMs Facilitate the Generation of EHR Phenotyping Algorithms*, medRxiv, PMC10775330.
- CELEC — *Reliable Curation of EHR Dataset via LLMs under Environmental Constraints*, arXiv:2511.00772.
- *The regulation of artificial intelligence in intensive care units*, npj Digital Medicine, 2026.
- *AI-Driven Radiology Report Generation for Traumatic Brain Injuries*, arXiv:2510.08498.
- *Generating synthetic EHR data using agent-based models for MCI robustness*, arXiv:2605.09951.
- AIPatient — *Simulated patient systems powered by LLM agents*, arXiv:2409.18924.

---

*本文档为方案级设计，落地代码以 `创伤失血性休克数字孪生原型/` 后续提交为准。*
