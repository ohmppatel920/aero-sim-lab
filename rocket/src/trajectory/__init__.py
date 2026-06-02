"""Trajectory simulation package for a 3-DOF launch model."""

from .models import SimulationInputs, SimulationOutputs
from .simulator import run_simulation

__all__ = ["SimulationInputs", "SimulationOutputs", "run_simulation"]
