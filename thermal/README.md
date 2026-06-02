# 1D Thermal Transient — Heated Wall Slab

Interactive tool for transient heat conduction through a wall: *When does the back face exceed a temperature limit?*

## Physics (plain English)

- Heat diffuses through a 1D slab with constant properties.
- Outer face (`x=0`) receives constant heat flux `q''`.
- Back face (`x=L`) is adiabatic.
- Explicit FTCS finite-difference solver with stability-checked timestep.

See [docs/model.md](docs/model.md) for equations and limitations.

## Quick start

From repo root:

```bash
streamlit run thermal/app.py
pytest thermal/tests -q
```

## Resume bullet

Built a 1D transient thermal conduction simulator with flux/adiabatic boundary conditions, stability-checked explicit FTCS solver, pytest validation, and Streamlit UI for time-to-limit analysis on a heated wall.

## Next upgrades

- Convection boundary at the hot face
- Temperature-dependent conductivity
- Link hot-face flux to a re-entry heat pulse profile
