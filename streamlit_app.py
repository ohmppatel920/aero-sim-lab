from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Aero Sim Lab",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Aero Sim Lab")
st.caption(
    "Interactive engineering-simulation demos — launch trajectory dynamics "
    "and transient wall heating."
)

st.markdown(
    """
Two small simulation tools with **documented governing equations**, **tested
numerical cores**, and interactive UIs for fast parameter exploration. Built to
show end-to-end engineering: physics model → numerical method → validation → UI.

Use the sidebar (**Rocket Trajectory** and **Thermal Slab**) to open each demo.
"""
)

left, right = st.columns(2)

with left:
    st.subheader("3-DOF Rocket Trajectory")
    st.markdown(
        """
Variable-mass point-mass flight with drag, max-q, and hybrid thrust alignment
(rail at low speed, velocity-aligned above a threshold).

- **Numerics:** RK4 integration
- **Validation:** pytest trend checks
- **Outputs:** apogee, range, max-q, impact time
"""
    )
    st.page_link("pages/1_Rocket_Trajectory.py", label="Open Rocket Trajectory →")

with right:
    st.subheader("1D Thermal Transient")
    st.markdown(
        """
Transient conduction through a wall with fixed surface heat flux and an
adiabatic back face. Reports the time to exceed a back-face temperature limit.

- **Numerics:** FTCS solver, stability-limited timestep
- **Validation:** pytest checks
- **Outputs:** T(x) profiles, back-face temperature, time-to-limit
"""
    )
    st.page_link("pages/2_Thermal_Slab.py", label="Open Thermal Slab →")

st.divider()
st.markdown(
    "Source code: [github.com/ohmppatel920/aero-sim-lab]"
    "(https://github.com/ohmppatel920/aero-sim-lab)"
)
