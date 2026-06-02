from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SimulationInputs:
    # Vehicle and launch parameters
    initial_mass_kg: float
    propellant_mass_kg: float
    thrust_newton: float
    burn_time_s: float
    drag_coefficient: float
    reference_area_m2: float
    launch_angle_deg: float
    thrust_align_speed_mps: float = 20.0  # rail thrust below this speed; velocity-aligned above

    # Environment and numerical settings
    g0_mps2: float = 9.80665
    rho0_kgm3: float = 1.225
    scale_height_m: float = 8500.0
    dt_s: float = 0.05
    max_time_s: float = 400.0


@dataclass(frozen=True)
class SimulationOutputs:
    time_s: np.ndarray
    x_m: np.ndarray
    z_m: np.ndarray
    vx_mps: np.ndarray
    vz_mps: np.ndarray
    mass_kg: np.ndarray
    speed_mps: np.ndarray
    dynamic_pressure_pa: np.ndarray
    apogee_m: float
    range_m: float
    max_q_pa: float
    burnout_time_s: float
    impact_time_s: float
