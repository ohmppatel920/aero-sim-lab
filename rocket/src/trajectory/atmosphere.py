import numpy as np


def density_exponential(altitude_m: float, rho0_kgm3: float, scale_height_m: float) -> float:
    """Simple exponential atmosphere model."""
    clamped_altitude = max(0.0, altitude_m)
    return rho0_kgm3 * np.exp(-clamped_altitude / scale_height_m)


def drag_force_newton(
    rho_kgm3: float, drag_coefficient: float, reference_area_m2: float, speed_mps: float
) -> float:
    """Compute drag magnitude using the quadratic drag model."""
    return 0.5 * rho_kgm3 * drag_coefficient * reference_area_m2 * speed_mps**2
