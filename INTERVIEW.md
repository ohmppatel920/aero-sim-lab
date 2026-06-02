# Interview prep — Aero Sim Lab

## Rocket project

**Assumptions:** 2D point mass; exponential atmosphere; quadratic drag; constant thrust magnitude; thrust along launch angle below 20 m/s then along velocity; no wind or attitude dynamics.

**Validation:** pytest checks impact after apogee, mass floor, thrust monotonicity on apogee.

**Limitation to mention:** No Mach-dependent drag or 6-DOF—next step would be `Cd(Mach)` table and pitch dynamics.

## Thermal project

**Assumptions:** 1D slab; constant k, rho, cp; fixed heat flux at hot face; adiabatic back face; explicit FTCS with stable timestep.

**Validation:** Higher flux heats faster; thicker wall delays back-face limit; finite stable temperatures.

**Limitation to mention:** No convection BC or temperature-dependent properties—next step is convective hot-face boundary.

## If asked "Did you write all the code?"

Yes—the physics cores are short first-principles implementations (~100–150 lines each), with tests and docs. Third-party libraries (NumPy, Streamlit, Plotly) handle numerics arrays and UI only; `.venv` is not in the repo.
