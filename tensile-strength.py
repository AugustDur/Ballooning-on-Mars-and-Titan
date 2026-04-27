global thickness, constants, area_density, multiplier

area_density = 0.7
multiplier = 0
possible_materials = []
max_strength = 7000000000


constants = {
    "g": 9.81,  # Gravitational acceleration, m/s^2
    "Cd": 0.45,  # Drag coefficient for a sphere
    "rho": 1.225,  # Air density at sea level, kg/m^3
    "rhom": 0.02,  # Density of the martian atmosphere, kg/m^3
    "Pm": 610,  # Pressure of atmosphere on mars, Pa
    "Pe": 101325,  # Pressure of atmosphere on earth, Pa
    "R": 8.314,  # Universal gas constant, J/(mol*K)
    "T": 210,  # Temperature on mars, K
    "M": 0.002,  # Molar mass of diatomic hydrogen, g/mol
    "rhog": 0.0899,  # Density of diatomic helium gas, kg/m^3
}

thickness = multiplier * area_density  # Thickness of the balloon material, m

def compute_tensile_strength(area_density, multiplier):
    thickness = multiplier * area_density  # Thickness of the balloon material, m
    radius = (3 * area_density) / (constants["rhom"] - ((constants["Pm"] * (constants["M"]) / (constants["R"] * constants["T"]))))
    tensile_strength_required = (constants["Pe"] - constants["Pm"]) * radius / (2 * thickness)
    return tensile_strength_required

for area_density in range (1, 1000):
    area_density = area_density / 1000
    for multiplier in range (1, 300):
        multiplier = multiplier / 100000
        tensile_strength_required = compute_tensile_strength(area_density, multiplier)
        if tensile_strength_required < max_strength:
            possible_materials.append((area_density, multiplier, tensile_strength_required))
        else:
            pass

print(len(possible_materials))

print(min(possible_materials, key=lambda x: x[2]))
print(max(possible_materials, key=lambda x: x[2]))