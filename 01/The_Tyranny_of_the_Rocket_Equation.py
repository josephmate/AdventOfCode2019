import sys
from functional import seq # from PyFunctional

lines = sys.stdin.readlines()
preprocessed = (seq(lines)
                  .map(lambda line: line.rstrip())
                  .map(lambda line: int(line))
                )
fuelForModules = (preprocessed
                # Fuel required to launch a given module is based on its mass.
                # Specifically, to find the fuel required for a module,
                # take its mass,
                # divide by three,
                # round down,
                # and subtract 2
                .map(lambda mass : (mass//3) - 2)
             ).sum()

print("Part 1: " + str(fuelForModules) + "\n")

def addOnFuelForFuel(moduleWeight):
    uncoveredFuelMass = moduleWeight
    fuelForFuel = 0
    while uncoveredFuelMass > 0:
        uncoveredFuelMass = (uncoveredFuelMass//3) - 2
        if uncoveredFuelMass > 0:
            fuelForFuel = fuelForFuel + uncoveredFuelMass
    return moduleWeight + fuelForFuel


fuelForModulesAndFuel = (preprocessed
                  .map(lambda mass : (mass//3) - 2)
                  # Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2.
                  # However, that fuel also requires fuel, and that fuel requires fuel, and so on.
                  # Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass,
                  # if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.
                  .map(addOnFuelForFuel)
                  ).sum()
print("Part 2: " + str(fuelForModulesAndFuel) + "\n")
