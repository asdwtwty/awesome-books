"""0D mechanistic cardiovascular model for traumatic hemorrhagic shock.

Two-compartment closed-loop circulation (systemic arterial + systemic venous)
with:
  - Frank-Starling stroke volume ~ stressed venous volume
  - Baroreflex modulation of heart rate and systemic vascular resistance
  - Hemorrhage source term (q_bleed) and resuscitation source term (q_iv)

Lineage: simplification of Ursino's haemorrhage / baroreflex models cited by
Hose et al. 2019 (Med Eng Phys) and Albanese-Cheng-Ursino-Chbat 2016 cited by
Sel et al. 2024 (JAHA).

Units
-----
time      : seconds
volume    : mL
pressure  : mmHg
flow      : mL / s
resistance: mmHg * s / mL  (PRU)
compliance: mL / mmHg
heart rate: bpm
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ModelParams:
    # Compliances
    C_a: float = 2.0       # systemic arterial
    C_v: float = 100.0     # systemic venous

    # Systemic vascular resistance baseline
    R_sys_0: float = 1.0   # PRU

    # Heart
    HR_0: float = 70.0     # bpm baseline
    SV_max: float = 110.0  # mL plateau stroke volume
    V_v_mid: float = 3500.0  # mL midpoint of the smooth preload sigmoid
    k_width: float = 600.0   # mL slope width of the preload sigmoid

    # Unstressed volumes (only used for compliance pressure terms)
    V_a_0: float = 700.0   # mL
    V_v_0: float = 2800.0  # mL

    # Baroreflex
    P_set: float = 90.0    # mmHg target MAP
    g_HR: float = 0.7      # bpm per mmHg of error
    g_R: float = 0.02      # PRU per mmHg of error
    tau_filt: float = 2.0  # s low-pass for sensed MAP

    # Physiological clipping
    HR_min: float = 40.0
    HR_max: float = 180.0
    R_min: float = 0.3
    R_max: float = 3.0
    SV_min: float = 5.0


def derived(state: np.ndarray, p: ModelParams) -> dict:
    """Compute algebraic outputs from the 3-D physiological state.

    state = [V_a, V_v, MAP_filt]
    """
    V_a, V_v, MAP_filt = state[0], state[1], state[2]

    P_a = max(0.0, (V_a - p.V_a_0) / p.C_a)
    P_v = max(0.0, (V_v - p.V_v_0) / p.C_v)

    err = p.P_set - MAP_filt
    HR = float(np.clip(p.HR_0 + p.g_HR * err, p.HR_min, p.HR_max))
    R_sys = float(np.clip(p.R_sys_0 + p.g_R * err, p.R_min, p.R_max))

    # Smooth, always-monotonic preload curve. Replaces the previous
    # max(V_v - V_v_0, 0) form whose zero-gradient plateau caused UKF
    # unobservability and divergence into unphysical V_v.
    z = (V_v - p.V_v_mid) / p.k_width
    sig = 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))
    SV = max(p.SV_max * sig, p.SV_min)

    CO = HR / 60.0 * SV          # mL / s
    Q_per = (P_a - P_v) / R_sys  # mL / s
    return {
        "P_a": P_a,
        "P_v": P_v,
        "HR": HR,
        "R_sys": R_sys,
        "SV": SV,
        "CO": CO,
        "Q_per": Q_per,
        "V_total": V_a + V_v,
    }


def rhs(state: np.ndarray, p: ModelParams, q_bleed: float, q_iv: float) -> np.ndarray:
    """Right-hand side of the ODE system."""
    d = derived(state, p)
    dV_a = d["CO"] - d["Q_per"]
    dV_v = d["Q_per"] - d["CO"] - q_bleed + q_iv
    dMAP = (d["P_a"] - state[2]) / p.tau_filt
    return np.array([dV_a, dV_v, dMAP], dtype=float)


def step_rk4(
    state: np.ndarray,
    p: ModelParams,
    dt: float,
    q_bleed: float,
    q_iv: float,
    n_substeps: int = 4,
) -> np.ndarray:
    """Advance the state by `dt` seconds using RK4 with optional substepping."""
    h = dt / n_substeps
    x = state.astype(float).copy()
    for _ in range(n_substeps):
        k1 = rhs(x, p, q_bleed, q_iv)
        k2 = rhs(x + 0.5 * h * k1, p, q_bleed, q_iv)
        k3 = rhs(x + 0.5 * h * k2, p, q_bleed, q_iv)
        k4 = rhs(x + h * k3, p, q_bleed, q_iv)
        x = x + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x
