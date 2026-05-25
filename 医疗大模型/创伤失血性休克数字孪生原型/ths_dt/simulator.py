"""Forward simulation, scenario builder and synthetic observation model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from .model import ModelParams, derived, step_rk4

ScenarioFn = Callable[[float], tuple[float, float]]


@dataclass
class Scenario:
    """Bleeding profile + (optional) externally supplied IV input.

    For a closed-loop run, q_iv is computed online by the controller and the
    `iv_fn` here can be a constant 0; for an open-loop comparison the user can
    pass an arbitrary q_iv profile.
    """
    bleed_fn: Callable[[float], float]
    iv_fn: Callable[[float], float]

    def __call__(self, t: float) -> tuple[float, float]:
        return float(self.bleed_fn(t)), float(self.iv_fn(t))


def ramp_then_hold(t_start: float, t_full: float, t_stop: float, q_max: float) -> Callable[[float], float]:
    """Hemorrhage profile: zero -> ramp -> hold @ q_max -> zero (after intervention)."""
    def f(t: float) -> float:
        if t < t_start:
            return 0.0
        if t < t_full:
            return q_max * (t - t_start) / max(t_full - t_start, 1e-9)
        if t < t_stop:
            return q_max
        return 0.0
    return f


def constant(value: float) -> Callable[[float], float]:
    return lambda _t: value


def simulate(
    params: ModelParams,
    scenario: Scenario,
    dt: float = 0.5,
    T: float = 360.0,
    x0: Optional[np.ndarray] = None,
):
    """Open-loop forward simulation."""
    if x0 is None:
        x0 = np.array([900.0, 4000.0, params.P_set])

    n = int(round(T / dt)) + 1
    times = np.linspace(0.0, T, n)
    states = np.zeros((n, 3))
    inputs = np.zeros((n, 2))
    states[0] = x0
    inputs[0] = scenario(times[0])
    for i in range(n - 1):
        q_b, q_iv = scenario(times[i])
        inputs[i] = (q_b, q_iv)
        states[i + 1] = step_rk4(states[i], params, dt, q_b, q_iv)
    inputs[-1] = scenario(times[-1])
    derived_log = [derived(s, params) for s in states]
    return times, states, derived_log, inputs


def observe(
    states: np.ndarray,
    params: ModelParams,
    sigma_map: float = 2.0,
    sigma_hr: float = 2.0,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Generate noisy bedside observations: [MAP, HR]."""
    rng = rng or np.random.default_rng(0)
    obs = np.zeros((len(states), 2))
    for i, s in enumerate(states):
        d = derived(s, params)
        obs[i, 0] = d["P_a"] + rng.normal(0.0, sigma_map)
        obs[i, 1] = d["HR"] + rng.normal(0.0, sigma_hr)
    return obs
