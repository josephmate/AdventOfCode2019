from functional import seq  # from PyFunctional

def countIndirectOrbits(directOrbitMap, orbitee):
    orbiters = directOrbitMap.get(orbitee)
    if orbiters is None:
        return (0, 0)

    totalChildren = 0
    totalIndirect = 0
    for orbiter in orbiters:
        (numChildren, numIndirect) = countIndirectOrbits(directOrbitMap, orbiter)
        totalChildren = totalChildren + numChildren + 1
        totalIndirect = totalIndirect + numIndirect
    totalIndirect = totalIndirect + totalChildren

    return (totalChildren, totalIndirect)


def solve(orbits):
    # build a map from orbitee to direct orbiters
    directOrbitMap = {}
    for (orbitee, orbiter) in orbits:
        # put if doesnt exist
        orbiters = directOrbitMap.get(orbitee)
        if orbiters is None:
            orbiters = set()
            directOrbitMap[orbitee] = orbiters
        # add to set
        orbiters.add(orbiter)

    (_, numOfIndirectOrbits) = countIndirectOrbits(directOrbitMap, "COM")
    return numOfIndirectOrbits

def parseAndSolve(lines):
    return solve((seq(lines)
            .map(lambda line: line.rstrip())
            .map(lambda line: line.split(")"))
            .map(lambda pair: (pair[0], pair[1]))
            .to_list()))

with open('input.small.txt', 'r') as fp:
    print("should print 42")
    print(str(parseAndSolve(fp.readlines())))

with open('input.txt', 'r') as fp:
    print("part 1")
    print(str(parseAndSolve(fp.readlines())))
