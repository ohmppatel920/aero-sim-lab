import os
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from trajectory.models import SimulationInputs
from trajectory.simulator import run_simulation


def _baseline_input() -> SimulationInputs:
    return SimulationInputs(
        initial_mass_kg=120.0,
        propellant_mass_kg=55.0,
        thrust_newton=2600.0,
        burn_time_s=18.0,
        drag_coefficient=0.45,
        reference_area_m2=0.02,
        launch_angle_deg=83.0,
    )


def test_simulation_returns_ground_impact_after_apogee() -> None:
    result = run_simulation(_baseline_input())
    assert result.apogee_m > 0.0
    assert result.impact_time_s > result.burnout_time_s
    assert result.z_m[-1] <= 0.0


def test_mass_decreases_to_dry_mass_and_not_below() -> None:
    input_data = _baseline_input()
    dry_mass = input_data.initial_mass_kg - input_data.propellant_mass_kg
    result = run_simulation(input_data)
    assert np.min(result.mass_kg) >= dry_mass - 1e-8
    max_discretization_error = (input_data.propellant_mass_kg / input_data.burn_time_s) * input_data.dt_s
    assert np.isclose(result.mass_kg[-1], dry_mass, atol=max_discretization_error + 1e-3)


def test_more_thrust_produces_higher_apogee() -> None:
    base = _baseline_input()
    weaker = SimulationInputs(**{**base.__dict__, "thrust_newton": 2200.0})
    stronger = SimulationInputs(**{**base.__dict__, "thrust_newton": 3200.0})
    low = run_simulation(weaker)
    high = run_simulation(stronger)
    assert high.apogee_m > low.apogee_m
