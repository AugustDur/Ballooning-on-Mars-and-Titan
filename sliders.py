"""Simulate and plot balloon velocity over time with interactive sliders."""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


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

STEP_MIN = 0.001
STEP_MAX = 0.02
STEP_STEP = 0.001

constants = {
    "g": 9.81,  # Gravitational acceleration, m/s^2
    "Cd": 0.45,  # Drag coefficient for a sphere
    "rho": 1.225,  # Air density at sea level, kg/m^3
    "rhom": 0.02,  # Density of the martian atmosphere, kg/m^3
    "Pm": 610,  # Pressure of atmosphere on mars, Pa
    "R": 8.314,  # Universal gas constant, J/(mol*K)
    "T": 210,  # Temperature on mars, K
    "M": 0.002,  # Molar mass of diatomic hydrogen, g/mol
    "rhog": 0.0899,  # Density of diatomic helium gas, kg/m^3
    "lambda": 0.7,  # Area density of the balloon, kg/m^2
}


def rebuild_balloon_values():
    global radius, balloon, mass, v_terminal

    radius = (3 * constants["lambda"]) / (
        constants["rhom"] - ((constants["Pm"] * constants["M"]) / (constants["R"] * constants["T"]))
    )

    balloon = {
        "Ax": 3.14 * radius**2,
        "As": 4 * 3.14 * radius**2,
        "Vol": (4 / 3) * 3.14 * radius**3,
    }

    mass = constants["lambda"] * balloon["As"] + constants["rhog"] * balloon["Vol"]
    v_terminal = (2 * (constants["rho"] * balloon["Vol"] - mass) * constants["g"] / (constants["Cd"] * constants["rho"] * balloon["Ax"])) ** 0.5


rebuild_balloon_values()


def solve_acceleration(velocity):
    # a = (Fb - mg - Fd) / m
    return (
        constants["rho"] * balloon["Vol"] * constants["g"]
        - mass * constants["g"]
        - 0.5 * constants["Cd"] * constants["rho"] * balloon["Ax"] * velocity**2
    ) / (mass)


def simulate(max_time, step):
    velocity = 0
    time_points = [0]
    velocity_points = [velocity]
    acceleration_points = [solve_acceleration(velocity)]

    for i in range(int(max_time / step)):
        acceleration = solve_acceleration(velocity)
        velocity += acceleration * step
        time = (i + 1) * step
        time_points.append(time)
        velocity_points.append(velocity)
        acceleration_points.append(solve_acceleration(velocity))

    return time_points, velocity_points, acceleration_points


def find_time_to_terminal_velocity(time_points, velocity_points, tolerance=0.01):
    for time, velocity in zip(time_points, velocity_points):
        if abs(velocity - v_terminal) <= tolerance:
            return time, velocity

    return time_points[-1], velocity_points[-1]


def main():
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.10, bottom=0.40)

    (velocity_line,) = ax.plot([], [], color="tab:blue", linewidth=2, label="Velocity")
    (acceleration_line,) = ax.plot([], [], color="tab:green", linewidth=2, label="Acceleration")
    terminal_point = ax.scatter([], [], s=90, color="purple", edgecolors="black", zorder=6, label="Time to terminal velocity")
    terminal_line = ax.axhline(0, color="tab:red", linestyle=":", linewidth=2, label="Terminal velocity")
    hover_annotation = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(12, 12),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.95),
        fontsize=9,
    )
    hover_annotation.set_visible(False)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s) / Acceleration (m/s²)")
    ax.set_title("Velocity and Acceleration vs Time")
    ax.grid(True)
    ax.legend(loc="lower right")

    lambda_ax = fig.add_axes([0.12, 0.30, 0.76, 0.03])
    cd_ax = fig.add_axes([0.12, 0.24, 0.76, 0.03])
    m_ax = fig.add_axes([0.12, 0.18, 0.76, 0.03])
    max_time_ax = fig.add_axes([0.12, 0.12, 0.76, 0.03])
    step_ax = fig.add_axes([0.12, 0.06, 0.76, 0.03])

    lambda_slider = Slider(
        lambda_ax,
        "lambda",
        LAMBDA_MIN,
        LAMBDA_MAX,
        valinit=DEFAULT_LAMBDA,
        valstep=LAMBDA_STEP,
    )
    cd_slider = Slider(
        cd_ax,
        "Cd",
        CD_MIN,
        CD_MAX,
        valinit=DEFAULT_CD,
        valstep=CD_STEP,
    )
    m_slider = Slider(
        m_ax,
        "M (g/mol)",
        M_VALUES[0],
        M_VALUES[-1],
        valinit=DEFAULT_M,
        valstep=M_VALUES,
    )
    max_time_slider = Slider(
        max_time_ax,
        "Max time (s)",
        MAX_TIME_MIN,
        MAX_TIME_MAX,
        valinit=DEFAULT_MAX_TIME,
        valstep=MAX_TIME_STEP,
    )
    step_slider = Slider(
        step_ax,
        "Step (s)",
        STEP_MIN,
        STEP_MAX,
        valinit=DEFAULT_STEP,
        valstep=STEP_STEP,
    )

    m_ax.set_xticks(M_VALUES)
    m_ax.set_xticklabels(["Hydrogen\n0.002", "Helium\n0.004"])
    m_ax.tick_params(axis="x", labelsize=8)

    current_time_points = []
    current_velocity_points = []
    current_acceleration_points = []

    def on_move(event):
        if event.inaxes != ax or not current_time_points or event.ydata is None:
            hover_annotation.set_visible(False)
            fig.canvas.draw_idle()
            return

        x = event.xdata
        if x is None:
            hover_annotation.set_visible(False)
            fig.canvas.draw_idle()
            return

        nearest_index = min(range(len(current_time_points)), key=lambda i: abs(current_time_points[i] - x))
        time_value = current_time_points[nearest_index]
        velocity_value = current_velocity_points[nearest_index]
        acceleration_value = current_acceleration_points[nearest_index]

        y_velocity = velocity_value
        y_acceleration = acceleration_value
        y_span = max(max(current_velocity_points), max(current_acceleration_points)) - min(min(current_velocity_points), min(current_acceleration_points))
        tolerance = max(0.01, 0.03 * y_span)

        nearest_distance = min(abs(event.ydata - y_velocity), abs(event.ydata - y_acceleration))
        if nearest_distance > tolerance:
            hover_annotation.set_visible(False)
            fig.canvas.draw_idle()
            return

        if abs(event.ydata - y_velocity) <= abs(event.ydata - y_acceleration):
            hover_text = f"t = {time_value:.3f} s\nv = {velocity_value:.3f} m/s"
            hover_xy = (time_value, velocity_value)
        else:
            hover_text = f"t = {time_value:.3f} s\na = {acceleration_value:.3f} m/s²"
            hover_xy = (time_value, acceleration_value)

        hover_annotation.xy = hover_xy
        hover_annotation.set_text(hover_text)
        hover_annotation.set_visible(True)
        fig.canvas.draw_idle()

    def on_leave(_):
        hover_annotation.set_visible(False)
        fig.canvas.draw_idle()

    def update(_):
        nonlocal current_time_points, current_velocity_points, current_acceleration_points

        constants["lambda"] = lambda_slider.val
        constants["Cd"] = cd_slider.val
        constants["M"] = m_slider.val
        rebuild_balloon_values()

        time_points, velocity_points, acceleration_points = simulate(
            max_time_slider.val,
            step_slider.val,
        )
        terminal_time, terminal_velocity = find_time_to_terminal_velocity(time_points, velocity_points)

        current_time_points = time_points
        current_velocity_points = velocity_points
        current_acceleration_points = acceleration_points

        velocity_line.set_data(time_points, velocity_points)
        acceleration_line.set_data(time_points, acceleration_points)
        terminal_line.set_ydata([v_terminal, v_terminal])
        terminal_point.set_offsets([[terminal_time, terminal_velocity]])
        terminal_point.set_label(f"time-to-terminal-velocity = {terminal_time:.3f} s")

        x_min, x_max = min(time_points), max(time_points)
        y_min = min(min(velocity_points), min(acceleration_points), v_terminal)
        y_max = max(max(velocity_points), max(acceleration_points), v_terminal)

        if y_max == y_min:
            y_padding = 1.0
        else:
            y_padding = 0.05 * (y_max - y_min)

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min - y_padding, y_max + y_padding)
        ax.legend(loc="lower right")
        fig.canvas.draw_idle()

    lambda_slider.on_changed(update)
    cd_slider.on_changed(update)
    m_slider.on_changed(update)
    max_time_slider.on_changed(update)
    step_slider.on_changed(update)
    fig.canvas.mpl_connect("motion_notify_event", on_move)
    fig.canvas.mpl_connect("figure_leave_event", on_leave)

    update(None)

    if plt.get_backend().lower() == "agg":
        fig.savefig("velocity_vs_time.png", dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()