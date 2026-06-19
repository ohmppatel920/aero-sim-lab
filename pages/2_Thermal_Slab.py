from __future__ import annotations

import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Repo root is the parent of this pages/ directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(REPO_ROOT, "thermal", "src"))

from thermal.models import SimulationInputs
from thermal.solver import run_simulation


def main() -> None:
    st.set_page_config(page_title="Thermal Slab Transient", page_icon="🔥", layout="wide")
    st.title("1D Thermal Transient — Heated Wall")
    st.caption("Heat conduction through a slab with fixed flux at the hot face and adiabatic back face.")

    with st.sidebar:
        st.header("Inputs")
        k = st.number_input("Conductivity k (W/m·K)", min_value=1.0, value=50.0, step=5.0)
        rho = st.number_input("Density rho (kg/m³)", min_value=100.0, value=7800.0, step=100.0)
        cp = st.number_input("Specific heat cp (J/kg·K)", min_value=100.0, value=500.0, step=50.0)
        thickness_m = st.number_input("Wall thickness (m)", min_value=0.001, value=0.01, step=0.001, format="%.3f")
        heat_flux = st.number_input("Surface heat flux q'' (W/m²)", min_value=1000.0, value=50000.0, step=5000.0)
        t0 = st.number_input("Initial temperature (K)", min_value=200.0, value=300.0, step=10.0)
        t_limit = st.number_input("Allowable back-face temp (K)", min_value=250.0, value=400.0, step=10.0)
        st.markdown("**Try this:** increase q'' or decrease thickness and watch time-to-limit drop.")

    sim_input = SimulationInputs(
        conductivity_w_mk=k,
        density_kg_m3=rho,
        specific_heat_j_kgk=cp,
        thickness_m=thickness_m,
        heat_flux_w_m2=heat_flux,
        initial_temp_k=t0,
        allowable_back_face_temp_k=t_limit,
    )
    outputs = run_simulation(sim_input)

    c1, c2, c3 = st.columns(3)
    c1.metric("Max back-face T", f"{outputs.max_back_face_temp_k:.1f} K")
    if outputs.time_to_limit_s is not None:
        c2.metric("Time to limit", f"{outputs.time_to_limit_s:.2f} s")
    else:
        c2.metric("Time to limit", "Not reached")
    c3.metric("Timestep dt", f"{outputs.dt_s*1000:.2f} ms")

    # Temperature profiles at a few times
    n_times = outputs.temperature_k.shape[0]
    sample_idx = [0, n_times // 4, n_times // 2, n_times - 1]
    profile_rows = []
    for idx in sample_idx:
        profile_rows.append(
            pd.DataFrame(
                {
                    "x_m": outputs.x_m,
                    "T_K": outputs.temperature_k[idx],
                    "time_s": outputs.time_s[idx],
                }
            )
        )
    profile_df = pd.concat(profile_rows, ignore_index=True)
    profile_df["time_label"] = profile_df["time_s"].map(lambda t: f"{t:.2f} s")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.line(
                profile_df,
                x="x_m",
                y="T_K",
                color="time_label",
                title="Temperature profile T(x) at selected times",
            ),
            use_container_width=True,
        )
    with right:
        back_df = pd.DataFrame(
            {"time_s": outputs.time_s, "back_face_T_K": outputs.back_face_temp_k}
        )
        st.plotly_chart(
            px.line(back_df, x="time_s", y="back_face_T_K", title="Back-face temperature vs time"),
            use_container_width=True,
        )


main()
