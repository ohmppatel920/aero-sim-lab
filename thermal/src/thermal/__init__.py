"""1D transient thermal conduction through a slab."""

from .models import SimulationInputs, SimulationOutputs
from .solver import run_simulation

__all__ = ["SimulationInputs", "SimulationOutputs", "run_simulation"]
