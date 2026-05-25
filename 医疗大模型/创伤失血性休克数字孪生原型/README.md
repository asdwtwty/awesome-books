# 机理-数据驱动融合的创伤失血性休克 (THS) 数字孪生 — 技术方案与最小化原型

> 本目录给出一个**可运行**的端到端最小原型,把上一份分析里推荐的技术路线落到代码:
> *0D 机理底座 + UKF 数据同化 + 闭环复苏控制器 + 虚拟队列 in-silico 沙盒*。
>
> 参考实现的方法学锚点都来自 [`asdwtwty/mechic-data-driven`](https://github.com/asdwtwty/mechic-data-driven) 仓库内的论文(下文逐处引用)。

---

## 1. 设计原则(为什么这么搭)

THS 的"快、稀、深"特点(决策快、数据稀、机制深)逼出三条硬约束:

| THS 约束 | 设计选择 | 来源 / 锚点论文 |
|---|---|---|
| 决策窗口分钟级,可获得信号只有 ABP/HR/SpO₂/POCUS | 0D 集总参数(LPM)做底座 — ms 级前向仿真 | Hose 2019(显式将 Ursino 失血模型列为 0D 个体化奠基);Sel 2024 JAHA |
| 数据稀疏、噪声大、参数个体差异极大 | UKF 顺序数据同化反演患者特异参数 + 出血率 | Kimmig 2025 FIMH(危重症 0D + ROUKF);Hose 2019(UKF 个体化) |
| 控制器需要安全验证,不能在真人上 RL 探索 | 机理孪生作为 in-silico 沙盒,控制器在虚拟队列上先跑 | Nair 2025(LSTM 决策 + 心脏 DT 闭环)|
| 失血复苏专属问题(允许性低血压、容量替代) | PI + 前馈替代估计出血率;DCR 目标 65–75 mmHg | Tivay & Hahn 2022 IEEE TBME(失血复苏个体化建模,被 Sel 2024 引用)|

> 一句话:**机理负责约束、解释、安全;数据驱动负责加速、个体化、决策**。这正是上一份分类里"机理-数据融合"格的具体落地。

---

## 2. 总体架构

```
┌───────────────────────────────────────────────────────────────────┐
│                      Real Patient (in vivo)                       │
│      ↓ ABP, HR, SpO₂, POCUS, lactate, Hb, ROTEM (sparse, noisy)   │
└─────────────────────────────┬─────────────────────────────────────┘
                              │  z_t = [MAP_obs, HR_obs]  (本原型)
                              ▼
┌───────────────────────────────────────────────────────────────────┐
│  ths_dt/ukf.py — Unscented Kalman Filter (Data Assimilation)      │
│  Augmented state: [V_a, V_v, MAP_filt, q_bleed]                   │
│  Process: ths_dt/model.py (RK4 step)                              │
│  Observation: hx -> [MAP, HR]                                     │
└─────────────────┬───────────────────────────┬─────────────────────┘
                  │ x̂ = (V_a, V_v, q_bleed)  │
                  ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│ ths_dt/controller.py     │   │ Decision support / monitoring    │
│ FluidPI: PI + FF(q_bleed)│   │ (estimated bleed rate, est. TBV, │
│   target = 65–75 mmHg    │   │  trend → trigger surgical / TXA) │
│   q_iv ∈ [0, 22] mL/s    │   └──────────────────────────────────┘
└─────────────┬────────────┘
              │ q_iv
              ▼
┌───────────────────────────────────────────────────────────────────┐
│  ths_dt/model.py — 0D mechanistic core (Ursino-style closed-loop) │
│  States: V_a, V_v, MAP_filt   Inputs: q_bleed, q_iv               │
│  • Frank-Starling preload (smooth sigmoid)                        │
│  • Baroreflex (HR, SVR modulated by sensed MAP)                   │
│  • Volume conservation                                            │
│  Acts as: (i) UKF process model, (ii) in-silico patient,          │
│  (iii) controller validation sandbox.                             │
└───────────────────────────────────────────────────────────────────┘
```

---

## 3. 各层技术选型与理由

### 3.1 机理底座 (`ths_dt/model.py`)

**两腔室闭环循环 + 失血源项 + 压力反射**:

- **状态变量**: `V_a`(动脉容量, mL), `V_v`(静脉容量, mL), `MAP_filt`(滤波后的平均动脉压, mmHg)
- **代数关系**: `P_a = (V_a − V_a_0)/C_a`, `P_v = (V_v − V_v_0)/C_v`
- **心脏**: 平滑 sigmoid 形 Frank-Starling(单调、永远可观测,避免硬 ReLU 平台带来的 UKF 发散)
  - `SV = SV_max · σ((V_v − V_v_mid)/k_width)`
  - `CO = HR/60 · SV`
- **压力反射**: `HR = HR_0 + g_HR·(P_set − MAP_filt)`, `R_sys = R_sys_0 + g_R·(P_set − MAP_filt)`(均带生理夹紧)
- **守恒**: `dV_a/dt = CO − Q_per`, `dV_v/dt = Q_per − CO − q_bleed + q_iv`

> ⚠️ 设计注记:用 `max(V_v − V_v_0, 0)` 的硬 ReLU 形 Frank-Starling 会在 V_v 落到不应力区时给出零梯度平台,UKF 跟踪会把 V_v 推到负值无穷以解释 MAP 下降(典型不可观测发散)。**改用 sigmoid 后这个失败模式消失**。这条经验对所有 0D + 数据同化的 THS 工作通用。

**血管参数缺省值**(覆盖男性成人):
| 参数 | 值 | 含义 |
|---|---|---|
| C_a | 2.0 mL/mmHg | 系统动脉顺应性 |
| C_v | 100 mL/mmHg | 系统静脉顺应性 |
| R_sys_0 | 1.0 PRU | 基线系统血管阻力 |
| HR_0 | 70 bpm | 基线心率 |
| SV_max | 110 mL | 最大每搏量 |
| V_v_mid | 3500 mL | 前负荷半饱和点 |
| g_HR / g_R | 0.7 / 0.02 | 反射增益 |

### 3.2 数据同化层 (`ths_dt/ukf.py`)

**Unscented Kalman Filter,联合状态-参数估计**:

- **增广状态**: `x = [V_a, V_v, MAP_filt, q_bleed]^T`
  - `q_bleed` 用随机游走建模:"我不知道病人现在出血多快,但它每秒可能变化几个 mL/s"
- **过程模型** `fx`: 调用 `step_rk4()` 一步,参数状态恒等映射 + 随机游走
- **观测模型** `hx`: 输出 `[MAP, HR]`
- **关键调参**:
  - `alpha = 0.5`(σ-点足够散开;1e-3 在 4 维下会导致 c≈0 退化为 EKF)
  - `Q[q_bleed, q_bleed] = 4.0·dt`(允许出血率快速变化)
  - `R = diag(4, 4) mmHg² / bpm²`(典型床边监护噪声)
  - **不**单独学 SVR offset:与 q_bleed 在 [MAP, HR] 上不可联合可识别(身上低血压等价于"低血容量"或"血管麻痹",信号在二者间退化分配),会让滤波器把所有 MAP 下降都解释为血管扩张,出血率永远停留在 0。这条结论沿用 Kimmig 2025 关于 ROUKF 状态选择的讨论。
- **可识别性约束**: 更新后强制 `q_bleed ≥ 0`, `V_a ∈ [200, 2500]`, `V_v ∈ [1500, 6000]`(基于生理上下界,防止线性化外推)

### 3.3 闭环控制器 (`ths_dt/controller.py`)

**PI + 前馈替代估计出血率**:

```
q_iv = clip( Kp·(MAP_target − MAP_est) + Ki·∫err dt + ff_gain·q̂_bleed,  0,  q_iv_max )
```

- `MAP_target = 70 mmHg`(损伤控制性复苏 DCR 的允许性低血压目标,出血未控前)
- `Kp = 1.5 mL/s/mmHg`, `Ki = 0.05`, 抗积分饱和 `±200`
- `ff_gain = 0.7`(部分替代):
  - **完全替代会让 q_bleed 不可观测!** 如果 IV 完全等于出血,MAP/HR 就回到基线,UKF 看不到任何残余信号。这是现实闭环系统的**根本观测性约束**,值得在临床用例里持续注意。
  - 部分替代保留可观测的 MAP 下降残差,既滴定到目标又持续校准 UKF。
- `q_iv_max = 22 mL/s ≈ 1.32 L/min`(快速推注的安全上限)
- 控制器**延迟启动**(`t > 180 s`):前 180 s 是开环检测,先让 UKF 锁定出血率,再切入闭环。这模拟了真实工作流"评估 → 决策 → 干预"的时序。

### 3.4 虚拟队列 in-silico 沙盒 (`examples/run_cohort.py`)

**生成 N 个虚拟病人,每人参数和出血强度都从分布里抽样**:

- 抽样:`R_sys_0`(N(1.0, 0.15))、`SV_max`(N(85, 12))、`HR_0`(N(72, 8))、`g_HR`(N(0.7, 0.15))、`g_R`(N(0.02, 0.005))、`V_v_0`(N(3000, 200))、`q_max`(N(11, 3) mL/s)
- 每个病人都用同一个 UKF + 控制器跑一遍闭环
- 报告:
  - 比例 `MAP_min > 50 mmHg`(硬安全底线)
  - 比例 `mean MAP ∈ [60, 75]` 在出血窗内(DCR 目标命中)
  - 总输入 IV / 总丢失血量 中位数(液体平衡)

> 这正是 **Nair 2025 (IEEE Access)** 把心脏数字孪生当成 in-silico 沙盒的做法:控制器先在虚拟队列上证明安全,再上真实病人。

---

## 4. 运行方式

```bash
# 安装依赖(只用了 numpy/scipy/matplotlib,纯 stdlib UKF)
pip install -r requirements.txt

# 单病人端到端 demo:出血 → UKF 检测 → 控制器复苏
PYTHONPATH=. python3 examples/run_demo.py
# -> examples/ths_demo.png

# 24 名虚拟病人队列:闭环安全验证
PYTHONPATH=. python3 examples/run_cohort.py
# -> examples/ths_cohort.png

# 模型物理合理性单元测试
PYTHONPATH=. python3 tests/test_model.py
```

### 4.1 单病人 demo 的预期输出

```
=== run summary ===
  MAE_bleed_open_loop_window_mL_s         :     1.77
  Bleed_est_at_ctrl_on_mL_s               :    10.85
  MAP_min_mmHg                            :    60.13
  MAP_mean_after_ctrl_mmHg                :    71.43
  Final_total_volume_mL                   :  4006.15
  Total_IV_given_mL                       :  1803.15
  Total_blood_lost_mL                     :  2697.00
```

解读:
- **出血率估计在开环窗口内 MAE = 1.77 mL/s**(真值 12 mL/s,15% 相对误差);控制器启动时刻,UKF 已经把出血率收敛到 **10.85 mL/s**。
- 没有干预下 MAP 跌到 **60 mmHg**(代偿失败的临床触发点),控制器启动后稳定在 **71 mmHg**(命中 DCR 目标带 65–75 mmHg)。
- 总输入液体 1803 mL < 总失血 2697 mL — **允许性低血压**策略下我们故意不做完全等量替代,等待手术止血。

### 4.2 队列 demo 的预期输出

```
cohort N=24
  fraction MAP_min > 50 mmHg          : 1.00
  fraction mean MAP in 60-75 in window: 0.88
  median total blood lost  [mL]       : 1916
  median total IV given    [mL]       : 1389
```

解读:24 名异质虚拟病人 100% 守住了 50 mmHg 硬底线,88% 命中 60-75 mmHg DCR 目标带。这就是 in-silico 安全验证的具体形态。

---

## 5. 与 mechic-data-driven 仓库论文的逐处对应

| 原型组件 | 对应论文 | 对应内容 |
|---|---|---|
| `model.py` 0D 闭环 + 反射 + 失血源项 | Hose 2019 "Cardiovascular models for personalised medicine" | 显式引用 Ursino 失血/baroregulation 模型作为 0D 个体化奠基 |
| `model.py` 整合心肺/CV 模型理念 | Sel 2024 JAHA "Building Digital Twins for Cardiovascular Health" | LPM/EM/FEM 谱系,引 Albanese-Cheng-Ursino-Chbat 心肺整合 |
| `ukf.py` 联合状态-参数估计 | Kimmig 2025 FIMH "Automatically Generated CV Digital Twin in Critical Care" | ROUKF 在 OR/ICU 实时反演 0D CV 参数,用 ABP/Doppler/ECG |
| `ukf.py` UKF 个体化方法论 | Hose 2019 | 用 Unscented Kalman Filter 把临床时间序列同化到 0D 模型 |
| `controller.py` + 虚拟沙盒 | Nair 2025 IEEE Access "Optimizing Inotropic Infusion ..." | LSTM/聚类 AI 决策 + 心脏 DT 作为 in-silico 闭环验证 |
| `controller.py` 失血复苏闭环 | Sel 2024 引用 Tivay & Hahn 2022 IEEE TBME | "Collective variational inference ... a case study on hemorrhage resuscitation" — 最贴近 THS 的种子文献 |
| 不确定性传播 + 后验保留 | Camps 2024(reaction-Eikonal Bayesian DT) | 贝叶斯反演保留参数后验,数据稀疏时仍可决策 |
| 机理参数 → 可解释 ML 特征 | Gu/Beard 2025 "Identification of digital twins to guide interpretable AI" | 机理孪生的参数本身作为下游 AI 特征 |
| 凝血扩展(本原型未实现) | de Vecchi 2026(ISTH 声明)| "Physics-anchored hybrid digital twins" 用于血栓与 TIC |
| 影像触发(本原型未实现) | Hussain 2022(ResNet-Attention ICH)| 合并 TBI 时孪生切换工作模式 |

---

## 6. 局限与下一步(roadmap to full system)

本原型刻意保持最小,但为完整临床级 THS 数字孪生留出了清晰的扩展点:

### 6.1 立即可做的扩展 (1-2 人月)
- **更多观测通道**: 加入 SpO₂、CVP、SVV/PPV、乳酸 — 直接修改 `hx()` 即可,UKF 框架自动复用。这能显著提高 q_bleed 的可观测性,缓解"完全前馈替代"的不可观测性问题。
- **凝血子模型**: 集成简化的 Hockin-Mann 凝血级联 + 纤溶,加入 ROTEM/TEG 同化通道,支持 TXA 与血制品决策(de Vecchi 2026 路线)。
- **氧输送模型**: 加 DO₂/VO₂ 隔室,以乳酸/碱缺失作为额外观测,把"组织灌注是否充分"显式建模。
- **真正的 RL 控制器**: 把 PI 替换为在虚拟队列上用 PPO/SAC 训练的 RL 代理,并在 in-silico 沙盒里通过通过率验证(Nair 2025 路线)。

### 6.2 中期扩展 (3-6 人月)
- **0D ↔ 1D 耦合**: 在大动脉损伤场景把主动脉用 1D Euler 替代,边界条件为 0D 心脏 + 0D 远端 Windkessel(Hose 2019 几何多尺度建模)。
- **PINN 替代模型**: 当床旁缺 IBP/POCUS 时,用 PINN 从 ECG + 无创 BP 推断 SV,补全观测向量(Thangaraj 2024 EHJ 综述提到的 Kashtanova/Jiang/Kuang 路线)。
- **影像触发器**: 集成 ResNet-Attention 风格的 ICH/FAST 分类器(Hussain 2022),触发"颅高压子模式"或"腹腔出血子模式"。
- **大规模虚拟预训练**: 仿 Ugurlu 2025 的 UK Biobank 路线,平时为高危人群预训练个体化孪生,创伤现场只做最小化更新。

### 6.3 工程与监管
- VVUQ(验证/确认/不确定性量化)流水线
- FDA SaMD / NMPA Ⅲ 类医疗器械监管对齐(Sarani Rad 2026 系统综述列出的实施障碍)
- 闭环安全联锁:UKF 后验方差超过阈值 → 自动退出闭环 → 报警

---

## 7. 文件结构

```
创伤失血性休克数字孪生原型/
├── README.md                       本技术方案
├── requirements.txt                numpy / scipy / matplotlib
├── ths_dt/
│   ├── __init__.py                 公共 API
│   ├── model.py                    0D 机理模型 + 失血源项 + 压力反射
│   ├── simulator.py                场景生成 + 同步观测器
│   ├── ukf.py                      自包含 UKF (4 维增广态)
│   └── controller.py               PI + 前馈复苏控制器
├── examples/
│   ├── run_demo.py                 单病人端到端演示
│   ├── run_cohort.py               24 名虚拟病人 in-silico 沙盒
│   ├── ths_demo.png                单病人结果图
│   └── ths_cohort.png              队列结果图
└── tests/
    └── test_model.py               物理合理性单元测试
```

---

## 8. 关键代码片段速览

**机理 + 数据 在每个时间步的耦合**(摘自 `examples/run_demo.py`):
```python
# 1) 真值病人前向(代表真实患者,机理模型)
x_true = step_rk4(x_true, p_true, dt, q_bleed_true, q_iv_applied)

# 2) 床旁观测(噪声)
z = [MAP_true + N(0, σ_MAP), HR_true + N(0, σ_HR)]

# 3) 数据同化:UKF 把观测同化到机理模型,反演 q_bleed
ukf.predict(dt, q_iv_applied)   # 机理前向 + 协方差传播
ukf.update(z)                   # 数据校正

# 4) 控制器:消费 UKF 估计,产生下一步干预
q_iv_applied = controller.step(MAP_est, q_bleed_est, dt)
```

这就是机理-数据驱动融合数字孪生最简洁的"生命循环"——下一步直接把它扩出去就是临床级系统。
