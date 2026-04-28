import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

max_strength = 7_500_000_000  # Pa, max tensile strength of carbon fiber
min_strength = 3_500_000_000  # Pa, min tensile strength of carbon fiber

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
min_strength_ratio = strength_constant / min_strength


multiplier_values = np.arange(1, 300, dtype=float) / 100000.0
tensile_strength_values = compute_tensile_strength(multiplier_values)

below_min = tensile_strength_values < min_strength
between_minmax = (tensile_strength_values >= min_strength) & (tensile_strength_values <= max_strength)
above_max = tensile_strength_values > max_strength

fig, ax = plt.subplots(figsize=(12, 7))
hover_annotation = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(12, 12),
    textcoords="offset points",
    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.95),
    fontsize=9,
)
hover_annotation.set_visible(False)

y_min = tensile_strength_values.min() * 0.9
y_max = tensile_strength_values.max() * 1.05
ymax_fraction = (np.log10(max_strength) - np.log10(y_min)) / (np.log10(y_max) - np.log10(y_min))

# Marker for realistic range on x-axis - will be added after axes are configured

ax.plot(
    multiplier_values[below_min],
    tensile_strength_values[below_min],
    color="green",
    linewidth=2,
    label="Below CF min range",
)
ax.scatter(
    multiplier_values[below_min],
    tensile_strength_values[below_min],
    s=18,
    alpha=0.75,
    c="green",
)
ax.scatter(
    multiplier_values[between_minmax],
    tensile_strength_values[between_minmax],
    s=18,
    alpha=0.75,
    c="green",
)
ax.scatter(
    multiplier_values[above_max],
    tensile_strength_values[above_max],
    s=24,
    alpha=0.85,
    c="red",
    marker="^",
    label="Above CF max",
)

# Exact point where the curve reaches the carbon-fiber max limit.
ax.scatter(
    [minimum_ratio],
    [max_strength],
    s=120,
    c="red",
    edgecolors="black",
    linewidths=1.2,
    zorder=5,
    label="CF max threshold",
)
ax.annotate(
    f"multiplier = {minimum_ratio:.5f}"
    + "\n(minimum ratio between thickness and area density)",
    xy=(minimum_ratio, max_strength),
    xytext=(0.58, 0.72),
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

# Split trendline at max_strength
below_bound = z_trend <= max_strength
above_bound = z_trend > max_strength

ax.plot(
    y_trend[below_bound],
    z_trend[below_bound],
    color="green",
    linewidth=2.2,
    label="Trendline",
)
ax.plot(
    y_trend[above_bound],
    z_trend[above_bound],
    color="red",
    linewidth=2.2,
)

ax.axhline(
    y=max_strength,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Carbon fiber upper bound tensile strength ({int(max_strength / 1_000_000)} MPa)",
)

ax.set_title("Tensile Strength of Balloon Material vs Alpha", fontsize=14)
ax.set_xlabel("Alpha")
ax.set_ylabel("Stress on Balloon (Pa)")
ax.set_yscale("log")
ax.set_xlim(multiplier_values.min(), multiplier_values.max())
ax.set_ylim(tensile_strength_values.min() * 0.9, tensile_strength_values.max() * 1.05)
ax.grid(True, which="both", alpha=0.25)

# Add x-axis marker for realistic range (looks like a number line with serifs)
y_bottom = tensile_strength_values.min() * 0.9
marker_height = (tensile_strength_values.min() * 0.9) * 0.02
serif_height = marker_height * 1.5

# Horizontal line
ax.plot(
    [0.0011, 0.00175],
    [y_bottom, y_bottom],
    color="gold",
    linewidth=3,
    clip_on=False,
    zorder=5,
)

# Serif marks (vertical lines at boundaries)
ax.vlines(
    [0.0011, 0.00175],
    y_bottom,
    y_bottom + serif_height,
    color="gold",
    linewidth=2.5,
    clip_on=False,
    zorder=5,
)

ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.5f}"))

legend_items = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="green", markersize=7, label="Within CF range"),
    Line2D([0], [0], marker="^", color="w", markerfacecolor="red", markersize=7, label="Above CF upper bound"),
    Line2D([0], [0], color="black", lw=2.2, label="Trendline"),
    Line2D([0], [0], color="gold", lw=3, label="realistic range for high-density carbon fiber composites"),
    Line2D([0], [0], color="red", lw=2, linestyle="--", label=f"CF upper bound tensile strength ({int(max_strength / 1_000_000)} MPa)"),
]
ax.legend(handles=legend_items, loc="upper right")


curve_x = multiplier_values
curve_y = tensile_strength_values


def on_move(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        hover_annotation.set_visible(False)
        fig.canvas.draw_idle()
        return

    point_pixels = ax.transData.transform(np.column_stack([curve_x, curve_y]))
    cursor_pixels = np.array([event.x, event.y])
    distances = np.hypot(point_pixels[:, 0] - cursor_pixels[0], point_pixels[:, 1] - cursor_pixels[1])
    nearest_index = int(np.argmin(distances))

    if distances[nearest_index] > 20:
        hover_annotation.set_visible(False)
        fig.canvas.draw_idle()
        return

    nearest_x = curve_x[nearest_index]
    nearest_y = curve_y[nearest_index]
    hover_annotation.xy = (nearest_x, nearest_y)
    hover_annotation.set_text(
        f"multiplier = {nearest_x:.5f}\nstrength = {nearest_y:.5f} Pa"
    )
    hover_annotation.set_visible(True)
    fig.canvas.draw_idle()


def on_leave(_):
    hover_annotation.set_visible(False)
    fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", on_move)
fig.canvas.mpl_connect("figure_leave_event", on_leave)

plt.tight_layout()
plt.show()
