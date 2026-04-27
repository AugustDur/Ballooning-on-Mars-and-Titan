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


# Sampling controls for faster plotting. Increase density for more detail.
AREA_STEP_INDEX = 20
MULTIPLIER_STEP_INDEX = 3


def compute_tensile_strength(area_density, multiplier):
    thickness = multiplier * area_density  # Thickness of the balloon material, m
    radius = (3 * area_density) / (
        constants["rhom"]
        - ((constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"]))
    )
    tensile_strength_required = (
        (constants["Pe"] - constants["Pm"]) * radius / (2 * thickness)
    )
    return tensile_strength_required


# Build a sampled 2D grid (area density x multiplier) and evaluate in one shot.
area_density_values = np.arange(100, 10000, AREA_STEP_INDEX, dtype=float) / 10000.0
multiplier_values = np.arange(1, 300, MULTIPLIER_STEP_INDEX, dtype=float) / 100000.0
x_area_density, y_multiplier = np.meshgrid(area_density_values, multiplier_values)
z_tensile_strength = compute_tensile_strength(x_area_density, y_multiplier)


x_flat = x_area_density.ravel()
y_flat = y_multiplier.ravel()
z_flat = z_tensile_strength.ravel()


below_cf = z_flat <= max_strength
above_cf = z_flat > max_strength

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    x_flat[below_cf],
    y_flat[below_cf],
    z_flat[below_cf],
    s=3,
    alpha=0.18,
    c="tab:blue",
    depthshade=False,
)
ax.scatter(
    x_flat[above_cf],
    y_flat[above_cf],
    z_flat[above_cf],
    s=4,
    alpha=0.35,
    c="tab:orange",
    marker="^",
    depthshade=False,
)

# Draw a horizontal CF threshold plane at z = max_strength.
x_plane, y_plane = np.meshgrid(
    [x_flat.min(), x_flat.max()],
    [y_flat.min(), y_flat.max()],
)
z_plane = np.full_like(x_plane, max_strength, dtype=float)
ax.plot_surface(x_plane, y_plane, z_plane, color="red", alpha=0.12, linewidth=0)

# Global trendline across all points (best 1/multiplier fit), shown at mean area density.
trend_constant = np.mean(z_flat * y_flat)
y_trend = np.linspace(y_flat.min(), y_flat.max(), 250)
x_trend = np.full_like(y_trend, x_flat.mean())
z_trend = trend_constant / y_trend
ax.plot(
    x_trend,
    y_trend,
    z_trend,
    color="black",
    linewidth=2.2,
)

ax.set_title("3D View: Area Density, Multiplier, and Required Tensile Strength")
ax.set_xlabel("Area Density")
ax.set_ylabel("Multiplier")
ax.set_zlabel("Required Tensile Strength (Pa)")
ax.view_init(elev=22, azim=-55)

legend_items = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="tab:blue", markersize=7, label="At or below CF max"),
    Line2D([0], [0], marker="^", color="w", markerfacecolor="tab:orange", markersize=7, label="Above CF max"),
    Line2D([0], [0], color="red", lw=3, alpha=0.4, label="CF max threshold plane (7.5e9 Pa)"),
    Line2D([0], [0], color="black", lw=2.2, label="Trendline (fit across all points)"),
]
ax.legend(handles=legend_items, loc="upper left")

plt.tight_layout()
plt.show()
