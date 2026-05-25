"""Unscented Kalman Filter for joint state-parameter estimation.

Augmented state: x = [V_a, V_v, MAP_filt, q_bleed]
  - V_a, V_v, MAP_filt : physiological state (model.py)
  - q_bleed            : current bleeding rate, modelled as random walk

This is a textbook UKF (Wan & van der Merwe 2000) without external deps so the
prototype stays self-contained. Methodologically aligned with Kimmig 2025 (FIMH)
ROUKF in critical care and Hose et al. 2019 UKF personalisation of CV models.

Note on identifiability: trying to additionally learn an SVR offset from
[MAP, HR] alone makes vasoplegia and hypovolemia degenerate explanations of the
MAP drop. The baroreflex in `model.py` already supplies dynamic SVR, so we
keep the parameter axis to the variable that actually has a clean signature
in slow MAP / volume dynamics — q_bleed.
"""
from __future__ import annotations

import numpy as np

from .model import ModelParams, derived, step_rk4

N_AUG = 4  # [V_a, V_v, MAP_filt, q_bleed]


def _sigma_points(
    x: np.ndarray, P: np.ndarray, alpha: float = 0.5, kappa: float = 0.0, beta: float = 2.0
):
    n = x.size
    lam = alpha ** 2 * (n + kappa) - n
    c = n + lam
    P_reg = P + 1e-9 * np.eye(n)
    try:
        sqrt_P = np.linalg.cholesky(c * P_reg)
    except np.linalg.LinAlgError:
        Ps = (P_reg + P_reg.T) / 2.0
        w, V = np.linalg.eigh(Ps)
        w = np.clip(w, 1e-9, None)
        sqrt_P = V @ np.diag(np.sqrt(c * w))
    sigmas = np.zeros((2 * n + 1, n))
    sigmas[0] = x
    for i in range(n):
        sigmas[i + 1] = x + sqrt_P[:, i]
        sigmas[n + i + 1] = x - sqrt_P[:, i]
    Wm = np.full(2 * n + 1, 0.5 / c)
    Wc = Wm.copy()
    Wm[0] = lam / c
    Wc[0] = lam / c + (1.0 - alpha ** 2 + beta)
    return sigmas, Wm, Wc


def fx(x: np.ndarray, dt: float, p: ModelParams, q_iv: float) -> np.ndarray:
    """Process model: physiological RK4 step + identity on parameter states."""
    state = x[:3]
    q_bleed = max(float(x[3]), 0.0)
    new_state = step_rk4(state, p, dt, q_bleed, q_iv)
    return np.concatenate([new_state, [x[3]]])


def hx(x: np.ndarray, p: ModelParams) -> np.ndarray:
    """Observation model: bedside sensors return [MAP, HR]."""
    state = x[:3]
    d = derived(state, p)
    return np.array([d["P_a"], d["HR"]])


class UKF:
    def __init__(
        self,
        params: ModelParams,
        x0: np.ndarray,
        P0: np.ndarray,
        Q: np.ndarray,
        R: np.ndarray,
    ):
        self.params = params
        self.x = x0.astype(float).copy()
        self.P = P0.astype(float).copy()
        self.Q = Q.astype(float).copy()
        self.R = R.astype(float).copy()

    # ---------- prediction ----------
    def predict(self, dt: float, q_iv: float) -> None:
        sigmas, Wm, Wc = _sigma_points(self.x, self.P)
        sigmas_f = np.array([fx(s, dt, self.params, q_iv) for s in sigmas])
        x_pred = (Wm[:, None] * sigmas_f).sum(axis=0)
        diff = sigmas_f - x_pred
        P_pred = self.Q.copy()
        for i in range(len(Wc)):
            P_pred += Wc[i] * np.outer(diff[i], diff[i])
        # Symmetrize for numerical stability
        P_pred = (P_pred + P_pred.T) / 2.0
        self.x, self.P = x_pred, P_pred
        self._sigmas_f = sigmas_f
        self._Wm = Wm
        self._Wc = Wc

    # ---------- update ----------
    def update(self, z: np.ndarray) -> None:
        sigmas_h = np.array([hx(s, self.params) for s in self._sigmas_f])
        z_pred = (self._Wm[:, None] * sigmas_h).sum(axis=0)
        diff_z = sigmas_h - z_pred
        diff_x = self._sigmas_f - self.x
        S = self.R.copy()
        Pxz = np.zeros((self.x.size, z.size))
        for i in range(len(self._Wc)):
            S += self._Wc[i] * np.outer(diff_z[i], diff_z[i])
            Pxz += self._Wc[i] * np.outer(diff_x[i], diff_z[i])
        K = Pxz @ np.linalg.inv(S)
        self.x = self.x + K @ (z - z_pred)
        self.P = self.P - K @ S @ K.T
        # Physiological constraints on the augmented state
        self.x[0] = float(np.clip(self.x[0], 200.0, 2500.0))      # V_a
        self.x[1] = float(np.clip(self.x[1], 1500.0, 6000.0))     # V_v
        self.x[3] = max(self.x[3], 0.0)                            # q_bleed >= 0
        self.P = (self.P + self.P.T) / 2.0
