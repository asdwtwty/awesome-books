"""Traumatic Hemorrhagic Shock (THS) Digital Twin — minimal hybrid prototype.

Layers
------
- model.py       : 0D mechanistic core (Ursino-style closed-loop CV + bleed + baroreflex)
- simulator.py   : forward integration + scenario / observation generation
- ukf.py         : Unscented Kalman Filter (joint state-parameter data assimilation)
- controller.py  : closed-loop fluid resuscitation controller (PI + feed-forward)

References (papers in `mechic-data-driven` repo):
- Kimmig et al. 2025 (FIMH)            -> 0D + sequential data assimilation in critical care
- Tivay & Hahn 2022 (IEEE TBME)        -> hemorrhage resuscitation, collective variational inference
- Hose et al. 2019 (Med Eng Phys)      -> UKF personalisation of CV models, cites Ursino haemorrhage work
- Nair et al. 2025 (IEEE Access)       -> AI decision + cardiac DT as in-silico sandbox
- Sel et al. 2024 (JAHA)               -> mechanism-as-foundation + multimodal data fusion
"""

from .model import ModelParams, derived, step_rk4
from .simulator import simulate, Scenario, observe
from .ukf import UKF
from .controller import FluidPI

__all__ = [
    "ModelParams",
    "derived",
    "step_rk4",
    "simulate",
    "Scenario",
    "observe",
    "UKF",
    "FluidPI",
]
