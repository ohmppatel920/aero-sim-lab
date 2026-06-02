from __future__ import annotations

import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from trajectory.models import SimulationInputs
from trajectory.simulator import run_simulation


def main() -> None:
    st.set_page_config(page_title="Rocket Trajectory Simulator", layout="wide")
    st.title("3-DOF Rocket Trajectory Simulator")
    st.caption("Point-mass ascent/coast model with drag, gravity, and propellant depletion.")

    with st.sidebar:
        st.header("Inputs")
        initial_mass_kg = st.number_input("Initial mass (kg)", min_value=20.0, value=120.0, step=5.0)
        propellant_mass_kg = st.number_input(
            "Propellant mass (kg)", min_value=5.0, value=55.0, step=1.0
        )
        thrust_newton = st.number_input("Thrust (N)", min_value=100.0, value=2600.0, step=100.0)
        burn_time_s = st.number_input("Burn time (s)", min_value=1.0, value=18.0, step=0.5)
        launch_angle_deg = st.slider("Launch angle (deg)", min_value=60, max_value=90, value=83)
        drag_coefficient = st.slider("Drag coefficient Cd", min_value=0.1, max_value=1.0, value=0.45)
        reference_area_m2 = st.number_input(
            "Reference area (m^2)", min_value=0.001, value=0.02, step=0.001, format="%.3f"
        )
        thrust_align_speed_mps = st.slider(
            "Thrust align speed (m/s)",
            min_value=5,
            max_value=200,
            value=20,
            help="Below this speed, thrust follows launch angle; above, thrust follows velocity.",
        )
        st.markdown("**Try this:** set align speed very high (rail) vs very low (velocity-aligned).")

    sim_input = SimulationInputs(
        initial_mass_kg=initial_mass_kg,
        propellant_mass_kg=propellant_mass_kg,
        thrust_newton=thrust_newton,
        burn_time_s=burn_time_s,
        drag_coefficient=drag_coefficient,
        reference_area_m2=reference_area_m2,
        launch_angle_deg=float(launch_angle_deg),
        thrust_align_speed_mps=float(thrust_align_speed_mps),
    )
    outputs = run_simulation(sim_input)

    metric_cols = st.columns(4)
    metric_cols[0].metric("Apogee", f"{outputs.apogee_m:,.0f} m")
    metric_cols[1].metric("Range", f"{outputs.range_m:,.0f} m")
    metric_cols[2].metric("Max q", f"{outputs.max_q_pa/1000:,.1f} kPa")
    metric_cols[3].metric("Impact time", f"{outputs.impact_time_s:,.1f} s")

    df = pd.DataFrame(
        {
            "time_s": outputs.time_s,
            "x_m": outputs.x_m,
            "z_m": outputs.z_m,
            "speed_mps": outputs.speed_mps,
            "q_pa": outputs.dynamic_pressure_pa,
            "mass_kg": outputs.mass_kg,
        }
    )

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.line(df, x="x_m", y="z_m", title="Trajectory (Downrange vs Altitude)"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(df, x="time_s", y="speed_mps", title="Speed vs Time"),
            use_container_width=True,
        )
    with right:
        st.plotly_chart(
            px.line(df, x="time_s", y="q_pa", title="Dynamic Pressure vs Time"),
            use_container_width=True,
        )
        st.plotly_chart(
            px.line(df, x="time_s", y="mass_kg", title="Mass vs Time"),
            use_container_width=True,
        )

    st.subheader("Sampled Output")
    st.dataframe(df.iloc[:: max(len(df) // 25, 1)].reset_index(drop=True), use_container_width=True)


if __name__ == "__main__":
    main()
