# Recursivly solving for the velocity of the balloon until it reaches terminal velocity. 

global recursion_depth
global precision

precision = 0.01        # Time interval
recursion_depth = 120   # Time limit, seconds

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

print(radius)