<<<<<<< Updated upstream
# Recursivly solving for the velocity of the balloon until it reaches terminal velocity. 

global recursion_depth, precision, radius, balloon, velocity
=======
"""Simulate and plot balloon velocity over time with interactive sliders."""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
>>>>>>> Stashed changes

velocity = 0

<<<<<<< Updated upstream
precision = 0.001        # Time interval
recursion_depth = 5   # Time limit, seconds

constants = {
    "g": 9.81,                          # Gravitational acceleration, m/s^2
    "Cd": 0.47,                         # Drag coefficient for a sphere
    "rho": 1.225,                       # Air density at sea level, kg/m^3
    "rhom": 0.02,                       # Density of the martian atmosphere, kg/m^3
    "Pm": 610,                          # Pressure of atmosphere on mars, Pa
    "R": 8.314,                         # Universal gas constant, J/(mol*K)
    "T": 210,                           # Temperature on mars, K
    "M": 0.002,                         # Molar mass of diatomic hydrogen, g/mol
    "rhog": 0.0899,                     # Density of diatomic helium gas, kg/m^3
    "lambda": 0.7,                      # Area density of the balloon, kg/m^2
}

radius = (3 * constants["lambda"]) / (constants["rhom"] - ((constants["Pm"] * (constants["M"]) / (constants["R"] * constants["T"]))))

balloon = {
    "Ax": 3.14 * radius**2,
    "As": 4 * 3.14 * radius**2,
    "Vol": (4/3) * 3.14 * radius**3
    }

mass = constants["lambda"] * balloon["As"] + constants["rhog"] * balloon["Vol"]

def solve_acceleration(velocity):
=======
DEFAULT_LAMBDA = 0.7
DEFAULT_CD = 0.47
DEFAULT_M = 0.002
DEFAULT_MAX_TIME = 5.0
DEFAULT_STEP = 0.001

LAMBDA_MIN = 0.2
LAMBDA_MAX = 1.6
LAMBDA_STEP = 0.01

CD_MIN = 0.4
CD_MAX = 0.6
CD_STEP = 0.01

M_VALUES = [0.002, 0.004]

MAX_TIME_MIN = 1.0
MAX_TIME_MAX = 30.0
MAX_TIME_STEP = 0.5

STEP_MIN = 0.00001
STEP_MAX = 0.002
STEP_STEP = 0.00001

CONSTANTS = {
    "g": 9.81,
    "rho": 1.225,
    "rhom": 0.02,
    "Pm": 610,
    "R": 8.314,
    "T": 210,
    "rhog": 0.0899,
}


def build_model(lambda_value, cd_value, molecular_mass):
    radius = (3 * lambda_value) / (
        CONSTANTS["rhom"]
        - ((CONSTANTS["Pm"] * molecular_mass) / (CONSTANTS["R"] * CONSTANTS["T"]))
    )

    balloon = {
        "Ax": 3.14 * radius**2,
        "As": 4 * 3.14 * radius**2,
        "Vol": (4 / 3) * 3.14 * radius**3,
    }

    mass = lambda_value * balloon["As"] + CONSTANTS["rhog"] * balloon["Vol"]
    buoyancy = CONSTANTS["rho"] * balloon["Vol"] * CONSTANTS["g"]
    weight = mass * CONSTANTS["g"]
    net_upward_force = buoyancy - weight
    terminal_velocity = 0.0

    if net_upward_force > 0:
        terminal_velocity = (net_upward_force / (cd_value * CONSTANTS["rho"] * balloon["Ax"])) ** 0.5

    return radius, balloon, mass, terminal_velocity


def solve_acceleration(velocity, model, cd_value):
    _, balloon, mass, _ = model
    drag = cd_value * CONSTANTS["rho"] * balloon["Ax"] * velocity * abs(velocity)
    return (
        CONSTANTS["rho"] * balloon["Vol"] * CONSTANTS["g"]
        - mass * CONSTANTS["g"]
        - drag
    ) / (2 * mass)
>>>>>>> Stashed changes

    # a = Fb - mg - Fd / m

    a = (constants['rho'] * balloon["Vol"] * constants["g"] - mass * constants["g"] - constants["Cd"] * constants["rho"] * balloon["Ax"] * velocity**2) / (2 * mass)
    print(a)
    
    return a

<<<<<<< Updated upstream
def main():

    velocity = 0

    for i in range(int(recursion_depth / precision)):
        velocity = solve_acceleration(velocity) * precision
        print(f"Time: {i * precision:.2f} s, Velocity: {velocity:.2f} m/s")
=======
def simulate(lambda_value, cd_value, molecular_mass, max_time, step):
    model = build_model(lambda_value, cd_value, molecular_mass)
    _, _, _, terminal_velocity = model

    time_points = [0.0]
    velocity_points = [0.0]
    velocity = 0.0
    current_time = 0.0

    steps = max(1, int(max_time / step))
    for _ in range(steps):
        acceleration = solve_acceleration(velocity, model, cd_value)
        velocity += acceleration * step
        current_time += step
        time_points.append(current_time)
        velocity_points.append(velocity)

    return time_points, velocity_points, terminal_velocity


def main():
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.10, bottom=0.40)

    (velocity_line,) = ax.plot([], [], color="tab:blue", linewidth=2, label="Velocity")
    terminal_line = ax.axhline(0, color="tab:red", linestyle=":", linewidth=2, label="Terminal velocity")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Velocity vs Time")
    ax.grid(True)
    ax.legend(loc="upper right")

    lambda_ax = fig.add_axes([0.12, 0.30, 0.76, 0.03])
    cd_ax = fig.add_axes([0.12, 0.24, 0.76, 0.03])
    m_ax = fig.add_axes([0.12, 0.18, 0.76, 0.03])
    max_time_ax = fig.add_axes([0.12, 0.12, 0.76, 0.03])
    step_ax = fig.add_axes([0.12, 0.06, 0.76, 0.03])

    lambda_slider = Slider(lambda_ax, "lambda", LAMBDA_MIN, LAMBDA_MAX, valinit=DEFAULT_LAMBDA, valstep=LAMBDA_STEP)
    cd_slider = Slider(cd_ax, "Cd", CD_MIN, CD_MAX, valinit=DEFAULT_CD, valstep=CD_STEP)
    m_slider = Slider(m_ax, "M (g/mol)", M_VALUES[0], M_VALUES[-1], valinit=DEFAULT_M, valstep=M_VALUES)
    max_time_slider = Slider(max_time_ax, "Max time (s)", MAX_TIME_MIN, MAX_TIME_MAX, valinit=DEFAULT_MAX_TIME, valstep=MAX_TIME_STEP)
    step_slider = Slider(step_ax, "Step (s)", STEP_MIN, STEP_MAX, valinit=DEFAULT_STEP, valstep=STEP_STEP)

    m_ax.set_xticks(M_VALUES)
    m_ax.set_xticklabels(["Hydrogen\n0.002", "Helium\n0.004"])
    m_ax.tick_params(axis="x", labelsize=8)

    def update(_):
        time_points, velocity_points, terminal_velocity = simulate(
            lambda_slider.val,
            cd_slider.val,
            m_slider.val,
            max_time_slider.val,
            step_slider.val,
        )

        velocity_line.set_data(time_points, velocity_points)
        terminal_line.set_ydata([terminal_velocity, terminal_velocity])

        ax.relim()
        ax.autoscale_view()
        ax.legend(loc="upper right")
        fig.canvas.draw_idle()

    lambda_slider.on_changed(update)
    cd_slider.on_changed(update)
    m_slider.on_changed(update)
    max_time_slider.on_changed(update)
    step_slider.on_changed(update)

    update(None)

    if plt.get_backend().lower() == "agg":
        fig.savefig("velocity_vs_time.png", dpi=150, bbox_inches="tight")
    else:
        plt.show()

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()