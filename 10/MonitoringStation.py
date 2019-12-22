import functools
import sys
from functional import seq  # from PyFunctional
import math

from past.builtins import cmp


def parseMap(lines):
    asteroids = []

    for r in range(0, len(lines)):
        line = lines[r]
        for c in range(0, len(line)):
            cell = line[c]
            if cell == "#":
                asteroids.append((r, c))

    return asteroids


def distance(r, c, coordinate):
    return math.sqrt((r - coordinate[0]) * (r - coordinate[0]) + (c - coordinate[1]) * (c - coordinate[1]))


def abs(a):
    if a < 0:
        return a * -1
    return a


def gcd(a, b):
    a = abs(a)
    b = abs(b)
    if a == 0:
        return b
    if b == 0:
        return a
    for i in range(min(a, b) + 1, 1, -1):
        if a % i == 0 and b % i == 0:
            return i
    return 1


def getMaxRC(coords):
    maxR = 0
    maxC = 0
    for (r, c) in coords:
        if r > maxR:
            maxR = r
        if c > maxC:
            maxC = c
    return maxR, maxC


def asteroidsToMap(asteroids):
    asteroidHitMap = {}
    for asteroid in asteroids:
        asteroidHitMap[asteroid] = 1
    return asteroidHitMap


def findVisibleAsteroids(r, c, asteroids):
    asteroidsSortedByDistance = asteroids.copy();
    if (r,c) in asteroidsSortedByDistance:
        asteroidsSortedByDistance.remove((r, c))
    asteroidsSortedByDistance.sort(key=lambda coordinate: distance(r, c, coordinate))

    (maxR, maxC) = getMaxRC(asteroids)
    asteroidHitMap = asteroidsToMap(asteroidsSortedByDistance)

    for asteroid in asteroidsSortedByDistance:
        if asteroidHitMap[asteroid] == 1:
            rvector = asteroid[0] - r
            cvector = asteroid[1] - c
            divisor = gcd(rvector, cvector)
            rvector = rvector // divisor
            cvector = cvector // divisor
            currentR = asteroid[0] + rvector
            currentC = asteroid[1] + cvector
            while (maxR >= currentR >= 0
                   and maxC >= currentC >= 0):
                if (currentR, currentC) in asteroidHitMap:
                    asteroidHitMap[(currentR, currentC)] = 0
                currentR = currentR + rvector
                currentC = currentC + cvector

    visibleAsteroids = []
    for key, value in asteroidHitMap.items():
        if value == 1:
            visibleAsteroids.append(key)

    return visibleAsteroids


def countVisibleAsteroids(r, c, asteroids):
    return len(findVisibleAsteroids(r, c, asteroids))


def calcAllVisibleCounts(asteroids):
    visibleCounts = {}
    for (r, c) in asteroids:
        visibleCounts[(r, c)] = countVisibleAsteroids(r, c, asteroids)
    return visibleCounts


def printAsteroidMap(asteroidsMap):
    (maxR, maxC) = getMaxRC(asteroidsMap.keys())
    for r in range(0, maxR + 1):
        for c in range(0, maxC + 1):
            if (r, c) in asteroidsMap:
                print("#", end="")
            else:
                print(".", end="")
        print()


def printAsteroids(asteroids):
    printAsteroidMap(asteroidsToMap(asteroids))


def printVisibleCounts(visibleCounts):
    (maxR, maxC) = getMaxRC(visibleCounts.keys())
    for r in range(0, maxR + 1):
        for c in range(0, maxC + 1):
            if (r, c) in visibleCounts:
                print(visibleCounts[(r, c)], end="")
            else:
                print(".", end="")
        print()


def findBestLocation(lines):
    asteroids = parseMap(lines)
    maxVisibleAsteroids = -1
    bestLocation = None

    visibleCounts = calcAllVisibleCounts(asteroids)

    for (coord, visibleAsteroids) in visibleCounts.items():
        if visibleAsteroids > maxVisibleAsteroids:
            maxVisibleAsteroids = visibleAsteroids
            bestLocation = coord

    return maxVisibleAsteroids, bestLocation


def getQuadrant(coord):
    if coord[0] < 0 and coord[1] >= 0:
        return 0
    if coord[0] >= 0 and coord[1] > 0:
        return 1
    if coord[0] > 0 and coord[1] <= 0:
        return 2
    return 3

print("-1,0 should have quadrant 0 == " + str(getQuadrant((-1, 0))))
print("-1,1 should have quadrant 0 == " + str(getQuadrant((-1, 1))))
print("0,1 should have quadrant  1 == " + str(getQuadrant((0, 1))))
print("1,1 should have quadrant  1 == " + str(getQuadrant((1, 1))))
print("1,0 should have quadrant  2 == " + str(getQuadrant((1, 0))))
print("1,-1 should have quadrant  2 == " + str(getQuadrant((1, -1))))
print("0,-1 should have quadrant  3 == " + str(getQuadrant((0, -1))))
print("-1,-1 should have quadrant  3 == " + str(getQuadrant((0, -1))))


def div(num, denom):
    if denom == 0:
        return sys.maxsize
    return abs(num) / abs(denom)


def verticalSlope(coord):
    return div(coord[0], coord[1])


def horizontalSlope(coord):
    return div(coord[1], coord[0])


#               -ve
#                |
#       3(-,-)   |        0 (-,+)
#                |
# -              |                 +
# v--------------+-----------------v
# e              |                 e
#       2(+,-)   |       1  (+,+)
#                |
#                |
#               +ve
def rotationalCompare(firstCoord, secondCoord):
    firstQuad = getQuadrant(firstCoord)
    secondQuad = getQuadrant(secondCoord)
    quadCmp = cmp(firstQuad, secondQuad)
    if not(quadCmp == 0):
        return quadCmp

    # at this point we know they are in the same quadrant
    if firstQuad == 0:
        return cmp(verticalSlope(secondCoord), verticalSlope(firstCoord))
    elif firstQuad == 1:
        return cmp(horizontalSlope(secondCoord), horizontalSlope(firstCoord))
    elif firstQuad == 2:
        return cmp(verticalSlope(secondCoord), verticalSlope(firstCoord))
    else: # firstQuad == 3:
        return cmp(horizontalSlope(secondCoord), horizontalSlope(firstCoord))

    return 0


# | a
# |
# |b
# +--
# my original sort was incorrect
# a should come before b
# but since we compare column before row, that doesn't happen
# as a result, i've added a D test case to some of the tests below
# -ve
#  |   D
#  |
#  |  B
#  A  C
#  |                 +
# -+-----------------v
#  |                 e
A = (-2, 0)
B = (-3, 2)
C = (-2, 2)
D = (-5, 3)
print(str(A) + " " + str(B) + " -1 == " + str(rotationalCompare(A, B)))
print(str(B) + " " + str(C) + " -1 == " + str(rotationalCompare(B, C)))
print(str(A) + " " + str(C) + " -1 == " + str(rotationalCompare(A, C)))
print(str(D) + " " + str(B) + " -1 == " + str(rotationalCompare(D, B)))
# --+-A---------------v
#   |                 e
#   | CB
#   |    D
#   |
#  +ve
A = (0, 2)
B = (2, 3)
C = (2, 2)
D = (3, 5)
print(str(A) + " " + str(B) + " -1 == " + str(rotationalCompare(A, B)))
print(str(B) + " " + str(C) + " -1 == " + str(rotationalCompare(B, C)))
print(str(A) + " " + str(C) + " -1 == " + str(rotationalCompare(A, C)))
print(str(D) + " " + str(B) + " -1 == " + str(rotationalCompare(D, B)))
# -              |
# v--------------+-
# e              |
#              C A
#              B |
#                |
#               +ve
A = (2, 0)
B = (3, -2)
C = (2, -2)
print(str(A) + " " + str(B) + " -1 == " + str(rotationalCompare(A, B)))
print(str(B) + " " + str(C) + " -1 == " + str(rotationalCompare(B, C)))
print(str(A) + " " + str(C) + " -1 == " + str(rotationalCompare(A, C)))
#               -ve
#                |
#                |
#             BC |
# -              |
# v------------A-+-
# e              |
A = (-2,  0)
B = (-3, -2)
C = (-2, -2)
print(str(A) + " " + str(B) + " -1 == " + str(rotationalCompare(A, B)))
print(str(B) + " " + str(C) + " -1 == " + str(rotationalCompare(B, C)))
print(str(A) + " " + str(C) + " -1 == " + str(rotationalCompare(A, C)))

def translateRotationalCompare(r, c):
    return lambda firstCoord, secondCoord: rotationalCompare((firstCoord[0] - r, firstCoord[1] - c),
                                                             (secondCoord[0] - r, secondCoord[1] - c))


def destroyAsteroidsInOrder(r, c, asteroids):
    asteroidsDestroyed = []
    asteroidsRemaining = set()
    for asteroid in asteroids:
        asteroidsRemaining.add(asteroid)
    asteroidsRemaining.remove((r, c))

    while len(asteroidsRemaining) > 0:
        asteroidsToDestroy = findVisibleAsteroids(r ,c, list(asteroidsRemaining))
        asteroidsToDestroy.sort(key=functools.cmp_to_key(translateRotationalCompare(r, c)))

        for asteroidToDestroy in asteroidsToDestroy:
            asteroidsDestroyed.append(asteroidToDestroy)
            asteroidsRemaining.remove(asteroidToDestroy)

    return asteroidsDestroyed


print(str(gcd(2, -1)))
asteroidStr = """.#..#
.....
#####
....#
...##"""
print(asteroidStr)
asteroidStr = asteroidStr.split("\n")
printAsteroids(parseMap(asteroidStr))
print("0,1 should be 7")
print(countVisibleAsteroids(0, 1, parseMap(asteroidStr)))
print("expected counts")
print(""".7..7
.....
67775
....7
...87""")
print("actual counts")
print(printVisibleCounts(calcAllVisibleCounts(parseMap(asteroidStr))))
print("3,4   8")
print(findBestLocation(asteroidStr))

asteroidStr = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
print(asteroidStr)
asteroidStr = asteroidStr.split("\n")
printAsteroids(parseMap(asteroidStr))
print("Best is 5,8 with 33 other asteroids detected")
print(countVisibleAsteroids(8, 5, parseMap(asteroidStr)))
print(findBestLocation(asteroidStr))

asteroidStr = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
print(asteroidStr)
asteroidStr = asteroidStr.split("\n")
printAsteroids(parseMap(asteroidStr))
print("Best is 1,2 with 35 other asteroids detected")
print(findBestLocation(asteroidStr))

asteroidStr = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
print(asteroidStr)
asteroidStr = asteroidStr.split("\n")
printAsteroids(parseMap(asteroidStr))
print("Best is 6,3 with 41 other asteroids detected")
print(findBestLocation(asteroidStr))

asteroidStr = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""".split("\n")
printAsteroids(parseMap(asteroidStr))
print("3, 8")
actuals = destroyAsteroidsInOrder(3, 8, parseMap(asteroidStr))
#  01234567890123456
# 0.#....###24...#..
# 1##...##.13#67..9#
# 2##...#...5.8####.
# 3..#.....X...###..
# 4..#.#.....#....##
print("(1, 8) == " + str(actuals[0]))
print("(0, 9) == " + str(actuals[1]))
print("(1, 9) == " + str(actuals[2]))
print("(0, 10) == " + str(actuals[3]))
print("(2, 9) == " + str(actuals[4]))


asteroidStr = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
print(asteroidStr)
asteroidStr = asteroidStr.split("\n")
printAsteroids(parseMap(asteroidStr))
print("Best is 11,13 with 210 other asteroids detected")
print(findBestLocation(asteroidStr))

actuals = destroyAsteroidsInOrder(13, 11, parseMap(asteroidStr))
print("12,11 == " + str(actuals[1-1]))
print("1,12 == " + str(actuals[2-1]))
print("2,12 == " + str(actuals[3-1]))
print("8,12 == " + str(actuals[10-1]))
print("0,16 == " + str(actuals[20-1]))
print("9,16 == " + str(actuals[50-1]))
print("16,10 == " + str(actuals[100-1]))
print("2,8 == " + str(actuals[200-1]))
print("9,10 == " + str(actuals[201-1]))
print("1,11 == " + str(actuals[299-1]))




with open('input.txt', 'r') as fp:
    lines = fp.readlines()
    print("Part 1")
    visibleAsteroidsCount, coordinates = findBestLocation(lines)
    print(str(visibleAsteroidsCount) + " " + str(coordinates))
    actuals = destroyAsteroidsInOrder(coordinates[0], coordinates[1], parseMap(lines))
    solution = actuals[200-1]
    print(str(solution))
    print(str(solution[1]*100 + solution[0]))


