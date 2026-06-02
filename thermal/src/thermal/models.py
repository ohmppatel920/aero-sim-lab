from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class SimulationInputs:
    # Material properties
    conductivity_w_mk: float  # k
    density_kg_m3: float  # rho
    specific_heat_j_kgk: float  # cp
    thickness_m: float  # L

    # Boundary / initial conditions
    heat_flux_w_m2: float  # q'' at x=0 (heated outer surface)
    initial_temp_k: float
    allowable_back_face_temp_k: float

    # Numerical settings
    num_nodes: int = 51
    max_time_s: float = 600.0
    stability_factor: float = 0.4  # fraction of FTCS stability limit


@dataclass(frozen=True)
class SimulationOutputs:
    time_s: np.ndarray
    x_m: np.ndarray
    temperature_k: np.ndarray  # shape (n_times, n_nodes)
    back_face_temp_k: np.ndarray
    time_to_limit_s: Optional[float]
    max_back_face_temp_k: float
    dt_s: float
    dx_m: float
