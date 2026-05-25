"""Closed-loop fluid resuscitation controller.

PI + feed-forward replacement of estimated bleeding rate. Anti-windup on the
integrator. The controller consumes the UKF's MAP estimate and the UKF's
estimated q_bleed (so it knows roughly how fast to keep up).

Methodological lineage: closed-loop fluid resuscitation reviewed by Gholami et
al. 2021 (cited by Nair 2025), with the cardiac digital twin acting as the
in-silico sandbox for safe controller validation (Nair et al. 2025).
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class FluidPI:
    target: float = 65.0       # mmHg, permissive hypotension target during DCR
    Kp: float = 1.5            # mL/s per mmHg
    Ki: float = 0.05           # mL/s per (mmHg*s)
    max_rate: float = 25.0     # mL/s ~ 1.5 L/min cap
    ff_gain: float = 1.0       # 1.0 = full bleed replacement
    integ: float = 0.0
    integ_clip: float = 200.0  # anti-windup

    def reset(self) -> None:
        self.integ = 0.0

    def step(self, map_est: float, q_bleed_est: float, dt: float, active: bool = True) -> float:
        if not active:
            return 0.0
        err = self.target - map_est
        self.integ = float(np.clip(self.integ + err * dt, -self.integ_clip, self.integ_clip))
        u = self.Kp * err + self.Ki * self.integ + self.ff_gain * max(q_bleed_est, 0.0)
        return float(np.clip(u, 0.0, self.max_rate))
