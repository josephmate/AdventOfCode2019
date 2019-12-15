import sys
from functional import seq  # from PyFunctional
import math


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
       return a*-1
   return a

def gcd(a, b):
    a = abs(a)
    b = abs(a)
    for i in range(min(a, b) + 1, 1, -1):
        if a % i == 0 and b % i == 0:
            return i
    return 1


def countVisibleAsteroids(r, c, asteroids):
    asteroidsSortedByDistance = asteroids.copy();
    asteroidsSortedByDistance.remove((r, c))
    asteroidsSortedByDistance.sort(key=lambda coordinate: distance(r, c, coordinate))

    maxR = 0
    maxC = 0
    asteroidHitMap = {}
    for asteroid in asteroidsSortedByDistance:
        asteroidHitMap[asteroid] = 1
        if asteroid[0] > maxR:
            maxR = asteroid[0]
        if asteroid[1] > maxC:
            maxC = asteroid[1]

    for asteroid in asteroidsSortedByDistance:
        if asteroidHitMap[asteroid] == 1:
            rvector = r - asteroid[0]
            cvector = c - asteroid[1]
            divisor = gcd(rvector, cvector)
            rvector = rvector // divisor
            cvector = cvector // divisor
            currentR = asteroid[0] + rvector
            currentC = asteroid[1] + cvector
            while (maxR >= currentR >= 0
                   and maxC >= currentC >= 0):
                if (currentR, currentC) in asteroidHitMap:
                    asteroidHitMap[(currentR, currentC)] = 0
                currentR = currentR + 1
                currentC = currentC + 1

    return sum(asteroidHitMap.values())


def findBestLocation(lines):
    asteroids = parseMap(lines)
    maxVisibleAsteroids = -1
    bestLocation = None

    for (r, c) in asteroids:
        visibleAsteroids = countVisibleAsteroids(r, c, asteroids)
        if visibleAsteroids > maxVisibleAsteroids:
            maxVisibleAsteroids = visibleAsteroids
            bestLocation = (r, c)

    return (maxVisibleAsteroids, bestLocation)


asteroidStr = """.#..#
.....
#####
....#
...##"""
asteroidStr = asteroidStr.split("\n")
print("3,4   8")
print(findBestLocation(asteroidStr))

print("expected counts")
print(""".7..7
.....
67775
....7
...87""")

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
asteroidStr = asteroidStr.split("\n")
print("Best is 5,8 with 33 other asteroids detected")
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
asteroidStr = asteroidStr.split("\n")
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
asteroidStr = asteroidStr.split("\n")
print("Best is 6,3 with 41 other asteroids detected")
print(findBestLocation(asteroidStr))

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
asteroidStr = asteroidStr.split("\n")
print("Best is 11,13 with 210 other asteroids detected")
print(findBestLocation(asteroidStr))

with open('input.txt', 'r') as fp:
    lines = fp.readlines()
    print("Part 1")
    print(findBestLocation(lines))
