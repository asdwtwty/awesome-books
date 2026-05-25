"""End-to-end THS digital twin demo.

Pipeline (every dt):
  1. true patient steps under hemorrhage profile + currently-applied IV
  2. bedside sensors emit noisy [MAP, HR]
  3. UKF predicts then updates -> joint estimate of (V_a, V_v, MAP_filt, q_bleed, dR_sys)
  4. PI+FF controller consumes the estimates and prescribes next IV rate

Plots a 4-panel figure to ths_demo.png:
  (a) MAP: truth / observed / UKF estimate / target band
  (b) total blood volume: truth vs UKF estimate
  (c) bleed rate: truth vs UKF estimate, IV rate overlaid
  (d) heart rate and SVR offset estimated by the UKF
"""
from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ths_dt import FluidPI, ModelParams, Scenario, UKF, derived, step_rk4
from ths_dt.simulator import constant, ramp_then_hold


HERE = Path(__file__).resolve().parent
OUT = HERE / "ths_demo.png"


def _equilibrium(p: ModelParams, T_settle: float = 120.0, dt: float = 0.5) -> np.ndarray:
    """Run the model with no bleed/IV until it reaches its closed-loop steady state."""
    x = np.array([900.0, 4000.0, p.P_set])
    n = int(round(T_settle / dt))
    for _ in range(n):
        x = step_rk4(x, p, dt, 0.0, 0.0)
    return x


def run(seed: int = 0, save_path: Path = OUT) -> dict:
    rng = np.random.default_rng(seed)
    p = ModelParams()

    dt = 0.5
    T = 480.0  # 8 minutes
    n = int(round(T / dt)) + 1
    times = np.linspace(0.0, T, n)

    # ----- Hemorrhage scenario: bleed starts at t=60 s, ramps to 12 mL/s, surgical
    # control at t=300 s. Controller activates at t=180 s, so the UKF first
    # observes 90 s of compensated -> decompensated shock, then the controller
    # stabilises the patient over the remaining bleed window and post-control.
    bleed = ramp_then_hold(t_start=60.0, t_full=90.0, t_stop=300.0, q_max=12.0)
    iv_open_loop = constant(0.0)  # controller will overwrite online
    scenario = Scenario(bleed_fn=bleed, iv_fn=iv_open_loop)

    # ----- True patient (slightly perturbed parameters vs the UKF model) -----
    # This emulates "the model is approximate; reality has structural mismatch".
    p_true = replace(p, R_sys_0=1.05, SV_max=100.0)
    # Initialise both truth and UKF prior near steady state so we don't see
    # transient settling artifacts at t=0.
    x_eq_true = _equilibrium(p_true)
    x_eq_model = _equilibrium(p)
    x_true = x_eq_true.copy()

    # ----- UKF init -----
    x0_aug = np.concatenate([x_eq_model, [0.0]])
    P0 = np.diag([50.0, 200.0, 9.0, 9.0])
    # Process noise: q_bleed is allowed to wander aggressively (random walk
    # interpretation of "we don't know how fast the patient is bleeding"); other
    # states have small process noise reflecting model trust.
    Q = np.diag([0.5, 5.0, 0.5, 4.0]) * dt
    R_obs = np.diag([4.0, 4.0])
    ukf = UKF(p, x0_aug.copy(), P0, Q, R_obs)

    # ----- Controller -----
    # ff_gain = 0.7 -> partial feed-forward replacement so a residual MAP
    # signature of ongoing bleed remains for the UKF (full replacement makes
    # q_bleed unobservable from MAP/HR alone, an interesting closed-loop
    # observability finding documented in the README).
    ctrl = FluidPI(target=70.0, Kp=1.5, Ki=0.05, max_rate=22.0, ff_gain=0.7)
    # Activate the controller only after a brief open-loop detection window so
    # the UKF first observes a clear MAP drop and then the controller stabilises.
    t_ctrl_on = 180.0

    # ----- Logs -----
    truth = np.zeros((n, 3))
    obs = np.zeros((n, 2))
    est = np.zeros((n, 4))
    bleed_log = np.zeros(n)
    iv_log = np.zeros(n)
    map_truth = np.zeros(n)
    hr_truth = np.zeros(n)
    sv_truth = np.zeros(n)
    co_truth = np.zeros(n)

    truth[0] = x_true
    est[0] = ukf.x
    d0 = derived(x_true, p_true)
    map_truth[0] = d0["P_a"]
    hr_truth[0] = d0["HR"]
    sv_truth[0] = d0["SV"]
    co_truth[0] = d0["CO"]
    obs[0] = (d0["P_a"], d0["HR"])

    q_iv = 0.0
    for i in range(n - 1):
        t = times[i]

        # 1) truth
        q_b = bleed(t)
        bleed_log[i] = q_b
        iv_log[i] = q_iv
        x_true = step_rk4(x_true, p_true, dt, q_b, q_iv)
        truth[i + 1] = x_true
        d_t = derived(x_true, p_true)
        map_truth[i + 1] = d_t["P_a"]
        hr_truth[i + 1] = d_t["HR"]
        sv_truth[i + 1] = d_t["SV"]
        co_truth[i + 1] = d_t["CO"]

        # 2) observation
        z = np.array(
            [
                d_t["P_a"] + rng.normal(0.0, 2.0),
                d_t["HR"] + rng.normal(0.0, 2.0),
            ]
        )
        obs[i + 1] = z

        # 3) UKF
        ukf.predict(dt, q_iv)
        ukf.update(z)
        est[i + 1] = ukf.x

        # 4) controller
        d_est = derived(ukf.x[:3], p)
        active = t > t_ctrl_on
        q_iv = ctrl.step(d_est["P_a"], max(ukf.x[3], 0.0), dt, active=active)

    bleed_log[-1] = bleed(times[-1])
    iv_log[-1] = iv_log[-2]

    # ---------- summary ----------
    # Evaluate UKF bleed estimation in the open-loop detection window.
    mask_open_loop = (times > 150.0) & (times < 180.0)
    mae_bleed = float(np.mean(np.abs(est[mask_open_loop, 3] - 12.0)))
    bleed_est_at_ctrl_on = float(est[int(t_ctrl_on / dt), 3])
    mask_bleed = (times > 90.0) & (times < 300.0)
    map_min = float(np.min(map_truth))
    map_after_ctrl = float(np.mean(map_truth[(times > 220.0) & (times < 300.0)]))
    final_volume = float(truth[-1, 0] + truth[-1, 1])
    summary = {
        "MAE_bleed_open_loop_window_mL_s": mae_bleed,
        "Bleed_est_at_ctrl_on_mL_s": bleed_est_at_ctrl_on,
        "MAP_min_mmHg": map_min,
        "MAP_mean_after_ctrl_mmHg": map_after_ctrl,
        "Final_total_volume_mL": final_volume,
        "Total_IV_given_mL": float(np.trapezoid(iv_log, times)),
        "Total_blood_lost_mL": float(np.trapezoid(bleed_log, times)),
    }
    print("=== run summary ===")
    for k, v in summary.items():
        print(f"  {k:40s}: {v:8.2f}")

    # ---------- plot ----------
    fig, axes = plt.subplots(4, 1, figsize=(10.5, 11), sharex=True)

    # (a) MAP
    ax = axes[0]
    ax.fill_between(times, 65, 75, color="#cfe8d4", alpha=0.6, label="DCR target band 65-75 mmHg")
    ax.axvline(t_ctrl_on, color="C2", ls=":", lw=1.0, alpha=0.8)
    ax.text(t_ctrl_on + 1, 105, "controller ON", color="C2", fontsize=8)
    ax.axvline(60, color="C3", ls=":", lw=1.0, alpha=0.8)
    ax.text(60 + 1, 105, "bleed start", color="C3", fontsize=8)
    ax.axvline(300, color="C0", ls=":", lw=1.0, alpha=0.8)
    ax.text(300 + 1, 105, "surgical control", color="C0", fontsize=8)
    ax.plot(times, map_truth, "k-", lw=1.4, label="MAP truth")
    ax.plot(times, obs[:, 0], color="0.55", lw=0.6, alpha=0.7, label="MAP observed (noisy)")
    p_est = (est[:, 0] - p.V_a_0) / p.C_a
    p_est = np.clip(p_est, 0, None)
    ax.plot(times, p_est, "C0--", lw=1.2, label="MAP UKF estimate")
    ax.axhline(p.P_set, color="0.7", lw=0.6, ls=":")
    ax.set_ylabel("MAP [mmHg]")
    ax.legend(loc="lower left", fontsize=8, ncol=2)
    ax.set_title("THS Digital Twin: hemorrhage detection + closed-loop fluid resuscitation")

    # (b) Total blood volume
    ax = axes[1]
    vol_true = truth[:, 0] + truth[:, 1]
    vol_est = est[:, 0] + est[:, 1]
    ax.plot(times, vol_true, "k-", lw=1.4, label="Total volume truth")
    ax.plot(times, vol_est, "C0--", lw=1.2, label="Total volume UKF estimate")
    ax.set_ylabel("Blood volume [mL]")
    ax.legend(loc="lower left", fontsize=8)

    # (c) Bleed and IV
    ax = axes[2]
    ax.plot(times, bleed_log, "C3-", lw=1.4, label="bleed truth")
    ax.plot(times, np.clip(est[:, 3], 0, None), "C3--", lw=1.2, label="bleed UKF estimate")
    ax.plot(times, iv_log, "C2-", lw=1.2, label="IV rate (controller)")
    ax.axvspan(60, 300, color="#fbe3e3", alpha=0.4)
    ax.set_ylabel("Flow [mL/s]")
    ax.legend(loc="upper left", fontsize=8, ncol=3)

    # (d) HR + bleed estimate confidence
    ax = axes[3]
    ax.plot(times, hr_truth, "C4-", lw=1.4, label="HR truth")
    ax.plot(times, obs[:, 1], color="0.55", lw=0.6, alpha=0.7, label="HR observed")
    ax.set_ylabel("HR [bpm]")
    ax.set_xlabel("time [s]")
    ax.legend(loc="upper left", fontsize=8)

    fig.tight_layout()
    fig.savefig(save_path, dpi=130)
    print(f"figure -> {save_path}")
    return summary


if __name__ == "__main__":
    run()
