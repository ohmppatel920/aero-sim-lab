# 1D Transient Thermal Slab Model

## Scope and assumptions

- One-dimensional heat conduction through a plane wall of thickness `L`.
- Uniform initial temperature `T0`.
- Outer surface at `x=0` sees constant heat flux `q''` (e.g., aerodynamic or engine heating).
- Back face at `x=L` is adiabatic (zero heat flux): `dT/dx = 0`.
- Constant material properties: `k`, `rho`, `cp` (no temperature-dependent properties).

## Governing equation

`dT/dt = alpha * d2T/dx2`, where `alpha = k / (rho * cp)`.

## Boundary conditions

- `x=0`: `-k * dT/dx = q''` (implemented with a ghost node).
- `x=L`: `dT/dx = 0` (adiabatic, enforced as `T[N] = T[N-1]` each step).

## Numerical method

- Explicit FTCS finite difference on a uniform grid.
- Stability requirement: `dt <= dx^2 / (2*alpha)`; default uses `0.4` of this limit.
- Simulation tracks back-face temperature `T(L,t)` and time to exceed an allowable limit.

## Validation checks

- Higher `q''` heats the back face faster.
- Thicker wall delays back-face heating.
- Solver remains stable (finite temperatures, no NaNs).

## Known limitations

- 1D only (no lateral gradients or fins).
- Constant properties; no phase change or radiation.
- Fixed flux BC only in v1 (no convection toggle yet).
