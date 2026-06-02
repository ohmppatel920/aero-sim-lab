# 3-DOF Rocket Model Notes

## Scope and assumptions
- Point-mass planar (x-z) 3-DOF kinematics with translational states only.
- Forces included: thrust, drag, and gravity.
- Thrust is aligned with launch angle while V < V_align
- Thrust is aligned with velocity when V >= V_align (simple gravity-turn apprx)
- Atmosphere is exponential: `rho = rho0 * exp(-z / H)`.
- Drag is quadratic: `D = 0.5 * rho * Cd * A * V^2`.
- Propellant burn is constant-mass-flow from `t=0` to `t=burn_time`.
- Simulation stops on ground impact after apogee crossing.

## State vector and equations
State vector: `[x, z, vx, vz, m]`

Kinematics:
- `dx/dt = vx`
- `dz/dt = vz`

Dynamics:
- `dvx/dt = (T*ux - D*ux) / m`
- `dvz/dt = (T*uz - D*uz) / m - g0`
- `dm/dt = -mdot` during burn, otherwise `0`

Where `[ux, uz]` is the unit vector along velocity, or launch direction at near-zero speed.

## Numerical method
- Explicit fixed-step RK4 integrator.
- Default time step `dt = 0.05 s`.
- Mass is hard-clamped at dry mass to avoid numerical undershoot.

## Validation checks included
- Ground impact occurs only after apogee crossing.
- Final mass equals dry mass.
- Increased thrust raises apogee (monotonic trend check).

## Known limitations
- No attitude dynamics or aerodynamic moments (not 6-DOF).
- No staging, winds, engine throttling, or gimbal control.
- No transonic wave-drag corrections or Mach-dependent Cd curve.
