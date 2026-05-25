"""In-silico virtual cohort: stress-test the controller across patient variability.

Each virtual patient has perturbed parameters (mass, vascular tone, reflex gain,
SV plateau) and a randomized bleeding rate. We measure:
  - whether MAP_min stayed above a hard floor (50 mmHg)
  - whether mean MAP within the bleeding window reached the DCR target band
  - total IV volume given vs total volume lost

This mirrors the role of the cardiac digital twin in Nair et al. 2025 (IEEE
Access) as an "in-silico sandbox" for safe AI-controller evaluation.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ths_dt import FluidPI, ModelParams, UKF, derived, step_rk4
from ths_dt.simulator import ramp_then_hold


HERE = Path(__file__).resolve().parent
OUT_PNG = HERE / "ths_cohort.png"


def run_one(seed: int, q_max: float, params_true: ModelParams, params_model: ModelParams) -> dict:
    rng = np.random.default_rng(seed)
    dt = 0.5
    T = 360.0
    n = int(round(T / dt)) + 1
    times = np.linspace(0.0, T, n)
    bleed = ramp_then_hold(60.0, 90.0, 240.0, q_max)

    # Equilibrate the truth model first so the run starts at steady state
    x_true = np.array([900.0, 4000.0, params_true.P_set])
    for _ in range(int(120.0 / dt)):
        x_true = step_rk4(x_true, params_true, dt, 0.0, 0.0)
    x_eq_model = np.array([900.0, 4000.0, params_model.P_set])
    for _ in range(int(120.0 / dt)):
        x_eq_model = step_rk4(x_eq_model, params_model, dt, 0.0, 0.0)

    x0_aug = np.concatenate([x_eq_model, [0.0]])
    P0 = np.diag([50.0, 200.0, 9.0, 9.0])
    Q = np.diag([0.5, 5.0, 0.5, 4.0]) * dt
    R_obs = np.diag([4.0, 4.0])
    ukf = UKF(params_model, x0_aug.copy(), P0, Q, R_obs)
    ctrl = FluidPI(target=70.0, Kp=1.5, Ki=0.05, max_rate=22.0, ff_gain=0.7)

    map_truth = np.zeros(n)
    iv_log = np.zeros(n)
    bleed_log = np.zeros(n)

    q_iv = 0.0
    d0 = derived(x_true, params_true)
    map_truth[0] = d0["P_a"]
    for i in range(n - 1):
        t = times[i]
        q_b = bleed(t)
        bleed_log[i] = q_b
        iv_log[i] = q_iv
        x_true = step_rk4(x_true, params_true, dt, q_b, q_iv)
        d_t = derived(x_true, params_true)
        map_truth[i + 1] = d_t["P_a"]
        z = np.array([d_t["P_a"] + rng.normal(0, 2.0), d_t["HR"] + rng.normal(0, 2.0)])
        ukf.predict(dt, q_iv)
        ukf.update(z)
        d_est = derived(ukf.x[:3], params_model)
        active = t > 70.0
        q_iv = ctrl.step(d_est["P_a"], max(ukf.x[3], 0.0), dt, active=active)
    bleed_log[-1] = bleed(times[-1])
    iv_log[-1] = iv_log[-2]

    mask_window = (times > 120.0) & (times < 240.0)
    return {
        "q_max": q_max,
        "MAP_min": float(np.min(map_truth)),
        "MAP_window_mean": float(np.mean(map_truth[mask_window])),
        "lost_mL": float(np.trapezoid(bleed_log, times)),
        "given_mL": float(np.trapezoid(iv_log, times)),
        "times": times,
        "map": map_truth,
    }


def main(n_patients: int = 24, save_path: Path = OUT_PNG) -> None:
    rng = np.random.default_rng(2026)
    nominal = ModelParams()
    results = []

    for k in range(n_patients):
        # patient variability vs nominal model
        scale = lambda mu, sd: float(rng.normal(mu, sd))
        p_true = replace(
            nominal,
            R_sys_0=np.clip(scale(1.0, 0.15), 0.6, 1.6),
            SV_max=np.clip(scale(85.0, 12.0), 55.0, 110.0),
            HR_0=np.clip(scale(72.0, 8.0), 55.0, 95.0),
            g_HR=np.clip(scale(0.7, 0.15), 0.3, 1.1),
            g_R=np.clip(scale(0.02, 0.005), 0.005, 0.04),
            V_v_0=np.clip(scale(3000.0, 200.0), 2400.0, 3500.0),
        )
        q_max = float(np.clip(rng.normal(11.0, 3.0), 5.0, 18.0))
        res = run_one(seed=k, q_max=q_max, params_true=p_true, params_model=nominal)
        results.append(res)

    # summary
    map_mins = np.array([r["MAP_min"] for r in results])
    in_band = np.mean([(60 <= r["MAP_window_mean"] <= 75) for r in results])
    above_floor = float(np.mean(map_mins > 50.0))
    print(f"cohort N={n_patients}")
    print(f"  fraction MAP_min > 50 mmHg          : {above_floor:.2f}")
    print(f"  fraction mean MAP in 60-75 in window: {in_band:.2f}")
    print(f"  median total blood lost  [mL]       : {np.median([r['lost_mL'] for r in results]):.0f}")
    print(f"  median total IV given    [mL]       : {np.median([r['given_mL'] for r in results]):.0f}")

    # plot spaghetti
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    for r in results:
        ax.plot(r["times"], r["map"], color="C0", alpha=0.35, lw=0.8)
    ax.axhline(65, color="C2", ls="--", lw=0.8, label="DCR target 65")
    ax.axhline(50, color="C3", ls="--", lw=0.8, label="hard floor 50")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("MAP [mmHg]")
    ax.set_title(f"In-silico cohort: closed-loop MAP (N={n_patients})")
    ax.legend(loc="lower right", fontsize=8)

    ax = axes[1]
    lost = np.array([r["lost_mL"] for r in results])
    given = np.array([r["given_mL"] for r in results])
    ax.scatter(lost, given, s=40, alpha=0.7)
    lim = max(lost.max(), given.max()) * 1.1
    ax.plot([0, lim], [0, lim], "0.6", ls="--", lw=0.8, label="given = lost")
    ax.set_xlabel("blood lost [mL]")
    ax.set_ylabel("IV given [mL]")
    ax.set_title("Volume balance per virtual patient")
    ax.legend(loc="upper left", fontsize=8)

    fig.tight_layout()
    fig.savefig(save_path, dpi=130)
    print(f"figure -> {save_path}")


if __name__ == "__main__":
    main()
