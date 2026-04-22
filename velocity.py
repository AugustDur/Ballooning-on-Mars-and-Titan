"""Simulate and plot balloon velocity over time."""

import matplotlib.pyplot as plt


precision = 0.001  # Time interval
recursion_depth = 5  # Time limit, seconds

constants = {
    "g": 9.81,  # Gravitational acceleration, m/s^2
    "Cd": 0.47,  # Drag coefficient for a sphere
    "rho": 1.225,  # Air density at sea level, kg/m^3
    "rhom": 0.02,  # Density of the martian atmosphere, kg/m^3
    "Pm": 610,  # Pressure of atmosphere on mars, Pa
    "R": 8.314,  # Universal gas constant, J/(mol*K)
    "T": 210,  # Temperature on mars, K
    "M": 0.002,  # Molar mass of diatomic hydrogen, g/mol
    "rhog": 0.0899,  # Density of diatomic helium gas, kg/m^3
    "lambda": 0.7,  # Area density of the balloon, kg/m^2
}

radius = (3 * constants["lambda"]) / (
    constants["rhom"]
    - ((constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"]))
)

balloon = {
    "Ax": 3.14 * radius**2,
    "As": 4 * 3.14 * radius**2,
    "Vol": (4 / 3) * 3.14 * radius**3,
}

mass = constants["lambda"] * balloon["As"] + constants["rhog"] * balloon["Vol"]
v_terminal = (2 * (mass * constants["g"] + constants["rho"] * balloon["Vol"] * constants["g"]) / (constants["Cd"] * constants["rho"] * balloon["Ax"])) ** 0.5

def solve_acceleration(velocity):
    # a = (Fb - mg - Fd) / m
    return (
        constants["rho"] * balloon["Vol"] * constants["g"]
        - mass * constants["g"]
        - constants["Cd"] * constants["rho"] * balloon["Ax"] * velocity**2
    ) / (2 * mass)


def main():
    velocity = 0
    time_points = [0]
    velocity_points = [velocity]

    for i in range(int(recursion_depth / precision)):
        acceleration = solve_acceleration(velocity)
        velocity += acceleration * precision
        time = (i + 1) * precision
        time_points.append(time)
        velocity_points.append(velocity)

    print(f"Final time: {time_points[-1]:.2f} s, Final velocity: {velocity_points[-1]:.2f} m/s")

    plt.plot(time_points, velocity_points)
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Time")
    plt.grid(True)
    if plt.get_backend().lower() == "agg":
        plt.savefig("velocity_vs_time.png", dpi=150, bbox_inches="tight")
    else:
        plt.show()


main()