from __future__ import annotations

import math
from typing import Tuple

import numpy as np

from .atmosphere import density_exponential, drag_force_newton
from .models import SimulationInputs, SimulationOutputs


def _dynamics(state: np.ndarray, t_s: float, sim_input: SimulationInputs) -> np.ndarray:
    x_m, z_m, vx_mps, vz_mps, mass_kg = state
    speed_mps = float(math.hypot(vx_mps, vz_mps))

    rho_kgm3 = density_exponential(z_m, sim_input.rho0_kgm3, sim_input.scale_height_m)
    drag_n = drag_force_newton(
        rho_kgm3, sim_input.drag_coefficient, sim_input.reference_area_m2, speed_mps
    )

    if t_s <= sim_input.burn_time_s and mass_kg > (sim_input.initial_mass_kg - sim_input.propellant_mass_kg):
        thrust_n = sim_input.thrust_newton
        mdot = sim_input.propellant_mass_kg / sim_input.burn_time_s
    else:
        thrust_n = 0.0
        mdot = 0.0

    if speed_mps > 1e-9:
        ux = vx_mps / speed_mps
        uz = vz_mps / speed_mps
    else:
        launch_rad = math.radians(sim_input.launch_angle_deg)
        ux = math.cos(launch_rad)
        uz = math.sin(launch_rad)

    launch_rad = math.radians(sim_input.launch_angle_deg)
    lx = math.cos(launch_rad)
    lz = math.sin(launch_rad)

    if speed_mps >= sim_input.thrust_align_speed_mps:
        tx, tz = ux, uz #velocity-aligned thrust
    else:
        tx, tz = lx, lz #launch-angle-aligned thrust

    thrust_x_n = thrust_n * tx
    thrust_z_n = thrust_n * tz
    drag_x_n = drag_n * ux
    drag_z_n = drag_n * uz

    ax_mps2 = (thrust_x_n - drag_x_n) / mass_kg
    az_mps2 = (thrust_z_n - drag_z_n) / mass_kg - sim_input.g0_mps2

    return np.array([vx_mps, vz_mps, ax_mps2, az_mps2, -mdot], dtype=float)


def _rk4_step(state: np.ndarray, t_s: float, dt_s: float, sim_input: SimulationInputs) -> np.ndarray:
    k1 = _dynamics(state, t_s, sim_input)
    k2 = _dynamics(state + 0.5 * dt_s * k1, t_s + 0.5 * dt_s, sim_input)
    k3 = _dynamics(state + 0.5 * dt_s * k2, t_s + 0.5 * dt_s, sim_input)
    k4 = _dynamics(state + dt_s * k3, t_s + dt_s, sim_input)
    return state + (dt_s / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def _initial_state(sim_input: SimulationInputs) -> np.ndarray:
    launch_rad = math.radians(sim_input.launch_angle_deg)
    return np.array([0.0, 0.0, 0.1 * math.cos(launch_rad), 0.1 * math.sin(launch_rad), sim_input.initial_mass_kg])


def _extract_outputs(
    states: np.ndarray, times: np.ndarray, sim_input: SimulationInputs
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    vx = states[:, 2]
    vz = states[:, 3]
    speed = np.sqrt(vx**2 + vz**2)
    rho = np.array(
        [density_exponential(z, sim_input.rho0_kgm3, sim_input.scale_height_m) for z in states[:, 1]]
    )
    q = 0.5 * rho * speed**2
    return speed, q, times


def run_simulation(sim_input: SimulationInputs) -> SimulationOutputs:
    dry_mass_kg = sim_input.initial_mass_kg - sim_input.propellant_mass_kg
    if dry_mass_kg <= 0:
        raise ValueError("Propellant mass must be less than initial mass.")
    if sim_input.burn_time_s <= 0 or sim_input.dt_s <= 0:
        raise ValueError("Burn time and time step must be positive.")

    states = [_initial_state(sim_input)]
    times = [0.0]
    apogee_crossed = False

    while times[-1] < sim_input.max_time_s:
        t_s = times[-1]
        next_state = _rk4_step(states[-1], t_s, sim_input.dt_s, sim_input)

        # Enforce dry mass floor.
        next_state[4] = max(dry_mass_kg, next_state[4])
        states.append(next_state)
        times.append(t_s + sim_input.dt_s)

        if states[-2][3] > 0 and next_state[3] <= 0:
            apogee_crossed = True

        if apogee_crossed and next_state[1] <= 0:
            break

    states_np = np.array(states)
    times_np = np.array(times)
    speed, q, _ = _extract_outputs(states_np, times_np, sim_input)

    z = states_np[:, 1]
    apogee_m = float(np.max(z))
    max_q_pa = float(np.max(q))

    burnout_time_s = min(sim_input.burn_time_s, float(times_np[-1]))
    impact_time_s = float(times_np[-1])
    range_m = float(max(0.0, states_np[-1, 0]))

    return SimulationOutputs(
        time_s=times_np,
        x_m=states_np[:, 0],
        z_m=states_np[:, 1],
        vx_mps=states_np[:, 2],
        vz_mps=states_np[:, 3],
        mass_kg=states_np[:, 4],
        speed_mps=speed,
        dynamic_pressure_pa=q,
        apogee_m=apogee_m,
        range_m=range_m,
        max_q_pa=max_q_pa,
        burnout_time_s=burnout_time_s,
        impact_time_s=impact_time_s,
    )
