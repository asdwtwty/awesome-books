# 创伤失血性休克伤员数字孪生 — 总体架构（图 1）

本文件给出"机理—数据双驱动伤员数字孪生"项目的总体技术架构，对应研究内容的三条主线：

1. 多分辨率（0D–1D–3D）可切换心血管系统建模
2. 机理模型与深度学习融合的失血性休克多生理系统建模
3. 基于便携式生命体征传感器的个性化高效参数辨识

整体分四层：**数据/知识输入 → 三大核心技术模块（呈数据闭环）→ 在线数字孪生 → 临床应用**。

## 架构图

```mermaid
flowchart TB
    classDef input    fill:#E3F2FD,stroke:#1976D2,color:#0D47A1
    classDef pillar1  fill:#FFF3E0,stroke:#F57C00,color:#E65100
    classDef pillar2  fill:#F3E5F5,stroke:#8E24AA,color:#4A148C
    classDef pillar3  fill:#E8F5E9,stroke:#43A047,color:#1B5E20
    classDef output   fill:#FFEBEE,stroke:#E53935,color:#B71C1C

    %% ============ INPUT LAYER ============
    subgraph IN[" 数据与知识输入层 "]
        direction LR
        SENS["便携式生命体征传感器<br/>HR · MAP · SpO₂ · ECG · 体温<br/>（实时观测流 z_k）"]:::input
        KNOW["创伤医学知识与数据<br/>生理机理方程 · 临床指南<br/>历史失血性休克病例库"]:::input
    end

    %% ============ CORE: THREE PILLARS ============
    subgraph CORE[" 机理—数据双驱动建模核心 "]
        direction LR

        %% ---- Pillar 1 ----
        subgraph P1["① 多分辨率高保真心血管系统"]
            direction TB
            CV0["0D 集中参数模型<br/>全身闭环循环 · 实时全局"]:::pillar1
            CV1["1D 大动脉网络<br/>压力/流量波传播"]:::pillar1
            CV3["3D CFD 局部血流<br/>关键脏器 / 受伤血管段"]:::pillar1
            CV0 <-. 救治阶段动态切换 .-> CV1
            CV1 <-. 精度-实时性平衡 .-> CV3
        end

        %% ---- Pillar 2 ----
        subgraph P2["② 机理—AI 混合多生理系统建模"]
            direction TB
            MECH["机理子模块（白盒）<br/>循环 ODE · 呼吸力学<br/>气体/物质交换"]:::pillar2
            PINN["物理约束深度网络（灰盒）<br/>神经反射 · 内分泌调节<br/>炎症级联"]:::pillar2
            JT["端到端联合训练<br/>L = L_physics + L_data"]:::pillar2
            MECH <--> PINN
            MECH --> JT
            PINN --> JT
        end

        %% ---- Pillar 3 ----
        subgraph P3["③ 基于传感器的个性化参数辨识"]
            direction TB
            AUG["状态-参数增广<br/>x̃_k = [x_k ; θ_k]"]:::pillar3
            UKF["无迹卡尔曼滤波（UKF）<br/>Sigma 点联合状态-参数估计"]:::pillar3
            UQ["参数后验 θ̂ + 协方差 P_θ<br/>（估计值 & 不确定度）"]:::pillar3
            AUG --> UKF --> UQ
        end

        %% ---- Inter-pillar data loop ----
        P1 ==血流动力学状态 x==> P2
        P2 ==模型预测观测 ŷ==> P3
        P3 ==个性化参数 θ̂ 反馈==> P1
        P3 ==个性化参数 θ̂ 反馈==> P2
    end

    %% ============ OUTPUT / APPLICATION ============
    subgraph OUT[" 在线伤员数字孪生与临床应用 "]
        direction LR
        TWIN["个性化伤员数字孪生<br/>实时同步真实伤员状态"]:::output
        PRED["伤情动态前瞻预测<br/>失代偿 / 休克进展 / 预后"]:::output
        DSS["分级救治决策支持<br/>液体复苏 · 止血时窗 · 转运分流"]:::output
        TWIN --> PRED --> DSS
    end

    %% ============ Cross-layer flows ============
    SENS ==实时观测 z_k==> P3
    KNOW --> P1
    KNOW --> P2
    P2 --> TWIN
    P3 --> TWIN
```

## 架构要点说明

### 1. 双驱动闭环（图中粗箭头构成的环）

这是整张图的灵魂：传感器 `z_k` → ③ UKF → 个性化参数 `θ̂` → 注入 ① 多分辨率 CV 模型 + ② 机理-AI 混合模型 → 模型生成预测观测 `ŷ` → 回到 ③ 做新一轮校正。三个研究内容并不是并列的三件事，而是**同一个数据-机理闭环上的三个功能位**。

### 2. 三大模块的角色定位

| 模块 | 角色 | 关键特性 |
|---|---|---|
| ① 多分辨率心血管 | **空间骨架** | 0D 全身实时 / 1D 波传播 / 3D 局部高保真，按救治阶段（院前→急救→ICU）切换 |
| ② 机理-AI 混合建模 | **生理广度** | 机理覆盖循环-呼吸；深度网络补建难以机理化的神经反射、内分泌、炎症级联 |
| ③ UKF 个性化辨识 | **时间适配** | 把通用模型快速"贴合"到当前伤员；输出 θ̂ 的同时给出不确定度，支持风险预测 |

### 3. 输入与输出的清晰分离

- 上方输入区强调"传感器实时流"和"医学知识/历史数据"两条独立来源，分别喂给在线辨识（③）和离线建模（①②）。
- 下方应用区把"孪生 → 预测 → 决策支持"做成一条递进链，对应技术成果到临床价值的转化路径。

### 4. 与本仓库现有原型的对应关系

| 架构组件 | 当前实现位置 | 状态 |
|---|---|---|
| ① 0D 心血管子模块 | `ths_dt/model.py`（V_a/V_v/MAP_filt 状态 + 简化压力反射） | 已实现最小版本 |
| ② 机理部分 | `ths_dt/model.py`（循环 ODE） | 已实现；AI 灰盒部分待补 |
| ③ UKF 联合估计 | `ths_dt/ukf.py`（增广状态 + Sigma 点） | 已实现最小可行版 |
| ① 1D/3D 切换层 | — | 待开发 |
| ② 物理约束神经网络 | — | 待开发 |
| ③ 多传感器融合 | — | 当前仅 [MAP, HR] 两路观测，待扩展 |
