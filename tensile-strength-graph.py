import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

max_strength = 7_500_000_000  # Pa, max tensile strength of carbon fiber

constants = {
    "g": 9.81,  # Gravitational acceleration, m/s^2
    "Cd": 0.45,  # Drag coefficient for a sphere
    "rho": 1.225,  # Air density at sea level, kg/m^3
    "rhom": 0.02,  # Density of the martian atmosphere, kg/m^3
    "Pm": 610,  # Pressure of atmosphere on Mars, Pa
    "Pe": 101325,  # Pressure of atmosphere on Earth, Pa
    "R": 8.314,  # Universal gas constant, J/(mol*K)
    "T": 210,  # Temperature on Mars, K
    "M": 0.002,  # Molar mass of diatomic hydrogen, g/mol
    "rhog": 0.0899,  # Density of diatomic helium gas, kg/m^3
}


# In this model, area density cancels out algebraically, so tensile strength depends
# only on multiplier.
def compute_tensile_strength(multiplier):
    denominator = constants["rhom"] - (
        (constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"])
    )
    return ((constants["Pe"] - constants["Pm"]) * 3) / (2 * denominator * multiplier)


denominator = constants["rhom"] - (
    (constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"])
)
strength_constant = ((constants["Pe"] - constants["Pm"]) * 3) / (2 * denominator)
minimum_ratio = strength_constant / max_strength


multiplier_values = np.arange(1, 300, dtype=float) / 100000.0
tensile_strength_values = compute_tensile_strength(multiplier_values)

below_cf = tensile_strength_values <= max_strength
above_cf = tensile_strength_values > max_strength

fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(
    multiplier_values[below_cf],
    tensile_strength_values[below_cf],
    color="tab:blue",
    linewidth=2,
    label="At or below CF max",
)
ax.scatter(
    multiplier_values[below_cf],
    tensile_strength_values[below_cf],
    s=18,
    alpha=0.75,
    c="tab:blue",
)
ax.scatter(
    multiplier_values[above_cf],
    tensile_strength_values[above_cf],
    s=24,
    alpha=0.85,
    c="tab:orange",
    marker="^",
    label="Above CF max",
)

# Exact point where the curve reaches the carbon-fiber limit.
ax.scatter(
    [minimum_ratio],
    [max_strength],
    s=120,
    c="gold",
    edgecolors="black",
    linewidths=1.2,
    zorder=5,
    label="Threshold point",
)
ax.annotate(
    f"multiplier = {minimum_ratio:.5f}"
    + "\n(minimum ratio between thickness and area density)",
    xy=(minimum_ratio, max_strength),
    xytext=(0.58, 0.82),
    textcoords="axes fraction",
    arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
    fontsize=10,
    ha="left",
    va="top",
    bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="gray", alpha=0.95),
)

# Trendline: the model is inversely proportional to multiplier, so this curve is the
# fitted relationship across all points.
y_trend = np.geomspace(multiplier_values.min(), multiplier_values.max(), 400)
z_trend = compute_tensile_strength(y_trend)
ax.plot(
    y_trend,
    z_trend,
    color="black",
    linewidth=2.2,
    label="Trendline",
)

ax.axhline(
    y=max_strength,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Carbon fiber max tensile strength (7.5e9 Pa)",
)

ax.set_title("Multiplier vs Required Tensile Strength")
ax.set_xlabel("Multiplier")
ax.set_ylabel("Required Tensile Strength (Pa)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(multiplier_values.min() * 0.9, multiplier_values.max() * 1.05)
ax.set_ylim(tensile_strength_values.min() * 0.9, tensile_strength_values.max() * 1.05)
ax.grid(True, which="both", alpha=0.25)

legend_items = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="tab:blue", markersize=7, label="At or below CF max"),
    Line2D([0], [0], marker="^", color="w", markerfacecolor="tab:orange", markersize=7, label="Above CF max"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="gold", markeredgecolor="black", markersize=8, label="Threshold point"),
    Line2D([0], [0], color="black", lw=2.2, label="Trendline"),
    Line2D([0], [0], color="red", lw=2, linestyle="--", label="CF max tensile strength (7.5e9 Pa)"),
]
ax.legend(handles=legend_items, loc="upper right")

plt.tight_layout()
plt.show()
