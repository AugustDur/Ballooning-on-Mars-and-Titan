# Recursivly solving for the velocity of the balloon until it reaches terminal velocity. 

global recursion_depth
global precision

precision = 0.01        # Time interval
recursion_depth = 120   # Time limit, seconds

constants = {
    "g": 9.81,           # Gravitational acceleration, m/s^2
    "Cd": 0.47,          # Drag coefficient for a sphere
    "r": 0.1,            # Radius of the balloon, m
    "rho": 1.225,        # Air density at sea level, kg/m^3
    "lambda": 0.7,       # Area density of the balloon, kg/m^2
}

def get_acceleration():

    # a = (Fb - mg - Fd) / m

    a = constants["g"] - (0.5 * constants["Cd"] * constants["A"] * constants["rho"] * v**2) / constants["m"]

    return a

def main():

    for i in range(recursion_depth/precision):

        a = get_acceleration(v)
        v += a * precision

        print(f"Time: {i*precision:.2f} s, Velocity: {v:.2f} m/s")

    if __name__ == "__main__":
        main()