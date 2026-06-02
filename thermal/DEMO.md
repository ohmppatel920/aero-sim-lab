# Thermal demo recording script (60–90 seconds)

1. Open app: `streamlit run thermal/app.py`
2. Show baseline back-face temperature curve and time-to-limit metric.
3. Increase heat flux `q''` — back face heats faster; time-to-limit drops.
4. Increase wall thickness — back face heats slower; time-to-limit increases.
5. Mention FTCS stability (timestep shown) and adiabatic back-face assumption from `docs/model.md`.

Save recording as `docs/demo-thermal.mp4` or link from portfolio README when ready.
