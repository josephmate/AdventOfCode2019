import sys
from functional import seq  # from PyFunctional

def parseInstructions(instructionStr):
    return (seq(instructionStr.split(","))
            .map(lambda instruction: (instruction[0], int(instruction[1:])))
            )

def solve(firstWireStr, secondWireStr):
    firstWire = parseInstructions(firstWireStr)
    wireHitLocation = {}
    signalDistanceMap = {}
    currentX = 0
    currentY = 0
    step = 0
    # indicate all spots the wire has hit
    for (direction, distance) in firstWire:
        xSpeed = 0
        ySpeed = 0
        if direction == "R":
            xSpeed = 1
        elif direction == "L":
            xSpeed = -1
        elif direction == "U":
            ySpeed = 1
        elif direction == "D":
            ySpeed = -1
        else:
            raise Exception("unrecogized direction: " + direction + str(distance))
        for i in range(1, distance + 1):
            step = step + 1
            currentX = currentX + xSpeed
            currentY = currentY + ySpeed
            if not(wireHitLocation.get((currentX, currentY), False)):
                signalDistanceMap[(currentX, currentY)] = step
            wireHitLocation[(currentX, currentY)] = True

    secondWire = parseInstructions(secondWireStr)
    closestCrossManhattanDistance = sys.maxsize
    closestSignalDistance = sys.maxsize
    currentX = 0
    currentY = 0
    step = 0
    for (direction, distance) in secondWire:
        xSpeed = 0
        ySpeed = 0
        if direction == "R":
            xSpeed = 1
        elif direction == "L":
            xSpeed = -1
        elif direction == "U":
            ySpeed = 1
        elif direction == "D":
            ySpeed = -1
        else:
            raise Exception("unrecogized direction: " + direction + str(distance))
        for i in range(1, distance + 1):
            step = step + 1
            currentX = currentX + xSpeed
            currentY = currentY + ySpeed

            if wireHitLocation.get((currentX, currentY), False):
                manhattanDistance = abs(currentX) + abs(currentY)
                if manhattanDistance < closestCrossManhattanDistance:
                    closestCrossManhattanDistance = manhattanDistance
                signalDistance = step + signalDistanceMap.get((currentX, currentY), sys.maxsize - step)
                if signalDistance < closestSignalDistance:
                    closestSignalDistance = signalDistance

    return (closestCrossManhattanDistance, closestSignalDistance)


print("expected (6, 30)")
print(solve("R8,U5,L5,D3",
            "U7,R6,D4,L4"))

print("expected (159, 610)")
print(solve("R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "U62,R66,U55,R34,D71,R55,D58,R83"))

print("expected (135, 410)")
print(solve("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))

with open('input.txt', 'r') as fp:
    firstWire = fp.readline().rstrip()
    secondWire = fp.readline().rstrip()
    print("Part 1:")
    print(str(solve(firstWire, secondWire)))
