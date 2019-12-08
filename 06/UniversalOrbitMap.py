import sys
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


def addOrbit(orbitMap, orbitee, orbiter):
    # put if doesnt exist
    orbiters = orbitMap.get(orbitee)
    if orbiters is None:
        orbiters = set()
        orbitMap[orbitee] = orbiters
    # add to set
    orbiters.add(orbiter)


def solvePart1(orbits):
    # build a map from orbitee to direct orbiters
    directOrbitMap = {}
    for (orbitee, orbiter) in orbits:
        addOrbit(directOrbitMap, orbitee, orbiter)

    (_, numOfIndirectOrbits) = countIndirectOrbits(directOrbitMap, "COM")
    return numOfIndirectOrbits


def parse(lines):
    return (seq(lines)
            .map(lambda line: line.rstrip())
            .map(lambda line: line.split(")"))
            .map(lambda pair: (pair[0], pair[1]))
            .to_list())


def parseAndSolvePart1(lines):
    return solvePart1(parse(lines))


def findShortestPath(directOrbitMap, visited, currentPlanet, destination):
    # reached out destination, nothing left to do
    if currentPlanet == destination:
        return 0

    # did not find a route
    orbiters = directOrbitMap.get(currentPlanet)
    if orbiters is None:
        return sys.maxsize

    visited.add(currentPlanet)
    shortestPath = sys.maxsize
    for orbiter in orbiters:
        if not(orbiter in visited):
            pathLength = findShortestPath(directOrbitMap, visited, orbiter, destination) + 1
            if pathLength < shortestPath:
                shortestPath = pathLength
    visited.remove(currentPlanet)

    return shortestPath


def solvePart2(orbits):
    # build a map from orbitee to direct orbiters
    directOrbitMap = {}
    for (orbitee, orbiter) in orbits:
        # need to be able to travel both directions
        addOrbit(directOrbitMap, orbitee, orbiter)
        addOrbit(directOrbitMap, orbiter, orbitee)

    # remove the two edges travelling from YOU to planet and planet to SAN
    return findShortestPath(directOrbitMap, set(), "YOU", "SAN") - 2


def parseAndSolvePart2(lines):
    return solvePart2(parse(lines))


with open('input.small.txt', 'r') as fp:
    print("should print 42")
    print(str(parseAndSolvePart1(fp.readlines())))

with open('input.txt', 'r') as fp:
    print("part 1")
    print(str(parseAndSolvePart1(fp.readlines())))

with open('input.small.part2.txt', 'r') as fp:
    print("should print 4")
    print(str(parseAndSolvePart2(fp.readlines())))

with open('input.txt', 'r') as fp:
    print("part 2")
    print(str(parseAndSolvePart2(fp.readlines())))
