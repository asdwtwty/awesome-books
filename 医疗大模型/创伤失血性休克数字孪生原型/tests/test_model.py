"""Sanity tests for the 0D model."""
from __future__ import annotations

import numpy as np

from ths_dt import ModelParams, derived, step_rk4
from ths_dt.simulator import Scenario, constant, ramp_then_hold, simulate


def _settle(p: ModelParams, T: float = 120.0, dt: float = 0.5):
    sc = Scenario(bleed_fn=constant(0.0), iv_fn=constant(0.0))
    times, states, dlog, _ = simulate(p, sc, dt=dt, T=T)
    return times, states, dlog


def test_baseline_steady_state():
    p = ModelParams()
    _, states, dlog = _settle(p)
    # MAP should settle near baroreflex set-point (within ~10 mmHg)
    assert 70.0 <= dlog[-1]["P_a"] <= 110.0
    # CO should be physiological (60-130 mL/s ~ 3.6-7.8 L/min)
    assert 50.0 <= dlog[-1]["CO"] <= 140.0
    # Volume conservation in absence of bleed/IV
    v0 = states[0, 0] + states[0, 1]
    v1 = states[-1, 0] + states[-1, 1]
    assert abs(v0 - v1) < 1.0


def test_hemorrhage_drops_map():
    p = ModelParams()
    sc = Scenario(bleed_fn=ramp_then_hold(30.0, 50.0, 200.0, 12.0), iv_fn=constant(0.0))
    times, states, dlog, _ = simulate(p, sc, dt=0.5, T=200.0)
    map_baseline = dlog[40]["P_a"]
    map_late = dlog[-1]["P_a"]
    # Sustained 12 mL/s bleed for ~150 s should drop MAP substantially
    assert map_late < map_baseline - 15.0
    # Reflex should drive HR up
    hr_baseline = dlog[40]["HR"]
    hr_late = dlog[-1]["HR"]
    assert hr_late > hr_baseline + 5.0
    # Total volume should monotonically decrease
    vol = states[:, 0] + states[:, 1]
    assert vol[-1] < vol[0] - 1000.0


def test_iv_replacement_restores_map():
    p = ModelParams()
    sc = Scenario(
        bleed_fn=ramp_then_hold(30.0, 50.0, 200.0, 8.0),
        iv_fn=constant(8.0),  # exact replacement
    )
    times, states, dlog, _ = simulate(p, sc, dt=0.5, T=200.0)
    map_late = dlog[-1]["P_a"]
    map_baseline = dlog[40]["P_a"]
    # With exact replacement, MAP should not collapse (within ~10 mmHg of baseline)
    assert abs(map_late - map_baseline) < 15.0


if __name__ == "__main__":
    test_baseline_steady_state()
    test_hemorrhage_drops_map()
    test_iv_replacement_restores_map()
    print("all model tests passed")
