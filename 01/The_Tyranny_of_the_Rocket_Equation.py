import sys
from functional import seq # from PyFunctional

lines = sys.stdin.readlines()
result = (seq(lines)
                .map(lambda line: line.rstrip())
                .map(lambda line: int(line))
                # Fuel required to launch a given module is based on its mass.
                # Specifically, to find the fuel required for a module,
                # take its mass,
                # divide by three,
                # round down,
                # and subtract 2
                .map(lambda mass : (mass//3) - 2)
             ).sum()

print(str(result) + "\n")


