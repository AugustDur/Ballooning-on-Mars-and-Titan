import matplotlib.pyplot as plt

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


def compute_tensile_strength(area_density, multiplier):
    thickness = multiplier * area_density  # Thickness of the balloon material, m
    radius = (3 * area_density) / (
        constants["rhom"]
        - ((constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"]))
    )
    tensile_strength_required = (
        (constants["Pe"] - constants["Pm"]) * radius / (2 * thickness)
    )
    return tensile_strength_required, radius


all_material_points = []

for area_density_step in range(100, 10000):
    area_density = area_density_step / 10000
    for multiplier_step in range(1, 300):
        multiplier = multiplier_step / 100000
        tensile_strength_required, radius = compute_tensile_strength(
            area_density, multiplier
        )
        all_material_points.append(
            (area_density, multiplier, tensile_strength_required, radius)
        )


x_area_density = [row[0] for row in all_material_points]
y_multiplier = [row[1] for row in all_material_points]
z_tensile_strength = [row[2] for row in all_material_points]
point_colors = ["tab:blue" if z < max_strength else "tab:orange" for z in z_tensile_strength]

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    x_area_density,
    y_multiplier,
    z_tensile_strength,
    s=1,
    alpha=0.2,
    c=point_colors,
)

# Draw a horizontal reference line at the carbon-fiber strength limit.
x_min, x_max = min(x_area_density), max(x_area_density)
y_max = max(y_multiplier)
ax.plot(
    [x_min, x_max],
    [y_max, y_max],
    [max_strength, max_strength],
    color="red",
    linestyle="--",
    linewidth=2,
    label="Carbon fiber max tensile strength (7.5e9 Pa)",
)

ax.set_title("3D View: Area Density, Multiplier, and Required Tensile Strength")
ax.set_xlabel("Area Density")
ax.set_ylabel("Multiplier")
ax.set_zlabel("Required Tensile Strength (Pa)")
ax.legend()
plt.tight_layout()
plt.show()
