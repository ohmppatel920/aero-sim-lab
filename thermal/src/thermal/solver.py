from __future__ import annotations

from typing import Optional

import numpy as np

from .models import SimulationInputs, SimulationOutputs


def _thermal_diffusivity(sim_input: SimulationInputs) -> float:
    return sim_input.conductivity_w_mk / (
        sim_input.density_kg_m3 * sim_input.specific_heat_j_kgk
    )


def _stable_timestep(dx_m: float, alpha_m2_s: float, stability_factor: float) -> float:
    limit = (dx_m**2) / (2.0 * alpha_m2_s)
    return stability_factor * limit


def run_simulation(sim_input: SimulationInputs) -> SimulationOutputs:
    if sim_input.num_nodes < 3:
        raise ValueError("num_nodes must be at least 3.")
    if sim_input.thickness_m <= 0:
        raise ValueError("thickness_m must be positive.")

    alpha = _thermal_diffusivity(sim_input)
    n = sim_input.num_nodes
    dx = sim_input.thickness_m / (n - 1)
    x = np.linspace(0.0, sim_input.thickness_m, n)
    dt = _stable_timestep(dx, alpha, sim_input.stability_factor)
    r = alpha * dt / (dx**2)

    if r > 0.5:
        raise ValueError(f"Unstable FTCS parameter r={r:.3f}; reduce dt or refine grid.")

    k = sim_input.conductivity_w_mk
    q = sim_input.heat_flux_w_m2

    t = 0.0
    temp = np.full(n, sim_input.initial_temp_k, dtype=float)
    times = [t]
    profiles = [temp.copy()]
    back_face = [temp[-1]]

    time_to_limit: Optional[float] = None

    while t < sim_input.max_time_s:
        t_old = temp.copy()
        temp_new = t_old.copy()

        # Ghost node for specified flux at x=0: -k*(T1 - Tm1)/(2*dx) = q
        ghost_left = t_old[1] + (2.0 * q * dx) / k

        for i in range(1, n - 1):
            temp_new[i] = t_old[i] + r * (t_old[i + 1] - 2.0 * t_old[i] + t_old[i - 1])

        temp_new[0] = t_old[0] + r * (t_old[1] - 2.0 * t_old[0] + ghost_left)
        # Adiabatic back face: zero gradient at x=L
        temp_new[-1] = temp_new[-2]

        temp = temp_new
        t += dt
        times.append(t)
        profiles.append(temp.copy())
        back_face.append(temp[-1])

        if time_to_limit is None and temp[-1] >= sim_input.allowable_back_face_temp_k:
            time_to_limit = t

        if time_to_limit is not None and t > time_to_limit + 5.0:
            break

    back_face_arr = np.array(back_face)
    return SimulationOutputs(
        time_s=np.array(times),
        x_m=x,
        temperature_k=np.array(profiles),
        back_face_temp_k=back_face_arr,
        time_to_limit_s=time_to_limit,
        max_back_face_temp_k=float(np.max(back_face_arr)),
        dt_s=dt,
        dx_m=dx,
    )
