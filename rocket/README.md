# Rocket Trajectory Simulator (3-DOF)

Interactive launch trajectory tool for exploring thrust, drag, and hybrid thrust alignment on apogee, range, and max dynamic pressure.

## What problem this solves

Given a simple sounding-rocket model, answer: *How high/far does it go, and what is peak aerodynamic load (max-q)?*

## Physics (plain English)

- Point mass in 2D with thrust, quadratic drag, and gravity.
- Mass decreases linearly during burn.
- Thrust follows launch angle at low speed, then aligns with velocity (simple gravity-turn approximation).
- Exponential atmosphere for air density vs altitude.

See [docs/model.md](docs/model.md) for equations, assumptions, and limitations.

## Quick start

From repo root (after `pip install -r requirements.txt`):

```bash
streamlit run rocket/app.py
pytest rocket/tests -q
```

## Demo script (60–90 s)

See [DEMO.md](DEMO.md) for a screen-recording outline.

## Resume bullet

Built a Python 3-DOF rocket trajectory simulator with variable mass, drag, hybrid thrust alignment, RK4 integration, pytest validation, and a Streamlit dashboard for real-time parameter exploration.

## Next upgrades

- Mach-dependent drag
- Wind profile
- Monte Carlo parameter uncertainty
