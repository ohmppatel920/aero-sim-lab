import numpy as np

from thermal.models import SimulationInputs
from thermal.solver import run_simulation


def _baseline_input() -> SimulationInputs:
    return SimulationInputs(
        conductivity_w_mk=50.0,
        density_kg_m3=7800.0,
        specific_heat_j_kgk=500.0,
        thickness_m=0.01,
        heat_flux_w_m2=50000.0,
        initial_temp_k=300.0,
        allowable_back_face_temp_k=400.0,
    )


def test_higher_heat_flux_heats_back_face_faster() -> None:
    base = _baseline_input()
    low = run_simulation(SimulationInputs(**{**base.__dict__, "heat_flux_w_m2": 30000.0}))
    high = run_simulation(SimulationInputs(**{**base.__dict__, "heat_flux_w_m2": 80000.0}))
    assert high.time_to_limit_s is not None
    assert low.time_to_limit_s is not None
    assert high.time_to_limit_s < low.time_to_limit_s


def test_thicker_wall_delays_back_face_heating() -> None:
    base = _baseline_input()
    thin = run_simulation(SimulationInputs(**{**base.__dict__, "thickness_m": 0.005}))
    thick = run_simulation(SimulationInputs(**{**base.__dict__, "thickness_m": 0.02}))
    assert thin.time_to_limit_s is not None
    assert thick.time_to_limit_s is not None
    assert thick.time_to_limit_s > thin.time_to_limit_s


def test_solver_runs_stable_without_nan() -> None:
    result = run_simulation(_baseline_input())
    assert np.all(np.isfinite(result.temperature_k))
    assert result.max_back_face_temp_k > result.back_face_temp_k[0]
    assert result.dt_s > 0.0
