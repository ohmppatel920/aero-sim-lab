# Aero Sim Lab

Two interactive **engineering simulation** demos for aerospace/mechanical portfolios: launch trajectory dynamics and transient wall heating.

| Project | Run | Docs |
|---------|-----|------|
| [Rocket 3-DOF trajectory](rocket/README.md) | `streamlit run rocket/app.py` | [rocket/docs/model.md](rocket/docs/model.md) |
| [1D thermal heated slab](thermal/README.md) | `streamlit run thermal/app.py` | [thermal/docs/model.md](thermal/docs/model.md) |

## Setup (once)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## What each project demonstrates

**Rocket** — Variable-mass point-mass flight with drag, max-q, and hybrid thrust alignment (rail at low speed, velocity-aligned above a threshold). RK4 integration + pytest trend checks.

**Thermal** — 1D transient conduction through a wall with fixed surface heat flux and adiabatic back face. FTCS solver with stability-limited timestep; reports time to exceed a back-face temperature limit.

## Portfolio pitch (30 seconds)

> I build small simulation tools with documented governing equations, tested numerical cores, and Streamlit UIs for fast parameter exploration—first launch mechanics, then thermal response of a heated structure.

## Resume bullets

- Built a Python 3-DOF rocket trajectory simulator (variable mass, drag, hybrid thrust alignment) with RK4 integration, pytest validation, and Streamlit dashboard.
- Built a 1D transient thermal conduction tool (flux/adiabatic BCs, FTCS solver) with stability-checked timestep and interactive time-to-limit analysis.

## Demo videos

Record using scripts in [rocket/DEMO.md](rocket/DEMO.md) and [thermal/DEMO.md](thermal/DEMO.md). Add screenshots or GIFs to each project README when ready.

## Repo layout

```
rocket/     # trajectory simulator
thermal/    # heated slab transient
requirements.txt
pytest.ini
```

Local virtual environments (`.venv/`) are gitignored—clone and `pip install` to reproduce.
