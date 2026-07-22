# Ballooning on Mars and Titan

A physics model for a gas-filled balloon (aerostat) descending through a thin planetary atmosphere — built around Mars's atmosphere, with Titan as an intended extension.

Given a target payload area density, the model:

1. Solves for the balloon's radius and mass from a force balance between buoyancy and the weight of the envelope + fill gas.
2. Numerically integrates the equations of motion — buoyancy, weight, and quadratic drag — to find velocity over time and how quickly the balloon reaches terminal velocity.
3. Separately checks whether the envelope material can actually survive the pressure differential between the balloon's interior and the surrounding atmosphere, by solving for the tensile strength required at a given thickness-to-area-density ratio and comparing it against the realistic range for high-density carbon fiber composites.

## Files

| File | What it does |
| --- | --- |
| `non-graphical.py` | The core simulation: recursively (Euler-integrates) solves for velocity over time until it converges on terminal velocity, printing progress to the console. Start here to understand the physics without any plotting dependencies. |
| `graphical.py` | Same simulation as `non-graphical.py`, refactored and plotted with matplotlib — outputs `velocity_vs_time.png`. |
| `sliders.py` | Interactive version of the velocity simulation with live matplotlib sliders for area density (`lambda`), drag coefficient (`Cd`), fill gas (hydrogen vs. helium), simulation length, and integration step size. Also plots acceleration and marks the time-to-terminal-velocity. |
| `tensile-strength.py` | Sweeps a range of area density / thickness ratios and reports which combinations keep the envelope's required tensile strength under a carbon-fiber strength ceiling. |
| `tensile-strength-graph.py` | Plots required tensile strength against the thickness-to-area-density ratio (alpha), with the realistic carbon-fiber composite strength range marked on the chart. Outputs a figure similar to `Tensile-strength-graph-v2.png`. |

## The physics

The balloon is modeled as a sphere with a thin shell of area density `lambda` (kg/m²), inflated with a fill gas (hydrogen or helium) to a radius set by the target atmospheric density. Terminal velocity comes from balancing:

- **Buoyancy** — the weight of atmosphere displaced by the balloon's volume
- **Weight** — the mass of the envelope plus the fill gas
- **Drag** — quadratic drag using a sphere's drag coefficient

against each other until net force reaches zero.

Separately, the envelope's required tensile strength is derived from the pressure differential between the inside and outside of the balloon (thin-wall pressure vessel: `σ = ΔP · r / (2t)`), which sets a hard constraint on how thin the material can be before it fails — independent of the velocity simulation.

## Running it

Requires `matplotlib` and `numpy`:

```bash
pip install matplotlib numpy
python non-graphical.py       # console output, no plotting
python graphical.py           # static velocity-vs-time plot
python sliders.py             # interactive sliders
python tensile-strength.py    # console output
python tensile-strength-graph.py   # tensile strength vs. thickness ratio plot
