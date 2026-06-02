import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from trajectory.models import SimulationInputs
from trajectory.simulator import run_simulation


def main() -> None:
    baseline = dict(
        initial_mass_kg=120.0,
        propellant_mass_kg=55.0,
        thrust_newton=2600.0,
        burn_time_s=18.0,
        drag_coefficient=0.45,
        reference_area_m2=0.02,
        launch_angle_deg=83.0,
    )
    rows = []
    for thrust in [2200, 2600, 3000, 3400]:
        for cd in [0.3, 0.45, 0.6]:
            sim_input = SimulationInputs(**{**baseline, "thrust_newton": thrust, "drag_coefficient": cd})
            out = run_simulation(sim_input)
            rows.append(
                {
                    "thrust_n": thrust,
                    "cd": cd,
                    "apogee_m": out.apogee_m,
                    "range_m": out.range_m,
                    "max_q_kpa": out.max_q_pa / 1000.0,
                    "impact_s": out.impact_time_s,
                }
            )

    df = pd.DataFrame(rows).sort_values(["cd", "thrust_n"]).reset_index(drop=True)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
