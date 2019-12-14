import sys
from functional import seq  # from PyFunctional


def countDigits(layer, digit):
    digitCount = 0
    for row in layer:
        for cell in row:
            if cell == digit:
                digitCount = digitCount + 1
    return digitCount


def solvePart1(layers):
    fewestZeros = sys.maxsize
    fewestZeroLayer = None

    for layer in layers:
        currentZeros = countDigits(layer, 0)
        if currentZeros < fewestZeros:
            fewestZeros = currentZeros
            fewestZeroLayer = layer

    return countDigits(fewestZeroLayer, 1) * countDigits(fewestZeroLayer, 2)


def assemble(line, width, height):
    numChars = len(line)
    idx = 0
    layers = []

    while idx < numChars:
        rows = []
        for row in range(0, height):
            row = []
            for column in range(0, width):
                row.append(int(line[idx]))
                idx = idx + 1
            rows.append(row)
        layers.append(rows)

    return layers

inputSmall = "123456789012"
smallWidth = 3
smallHeight = 2
print(str(solvePart1(assemble(inputSmall, smallWidth, smallHeight))))

def emptyLayer(width, height):
    layerSoFar = []
    for row in range(0, height):
        row = []
        for column in range(0, width):
            row.append(0)
        layerSoFar.append(row)
    return layerSoFar

def decodeImage(layers, width, height):
    layers.reverse()
    layerSoFar = emptyLayer(width, height)

    for layer in layers:
        for rowIdx in range(0, height):
            layerSoFarRow = layerSoFar[rowIdx]
            currentRow = layer[rowIdx]
            for columnIdx in range(0, width):
                layerSoFarCell = layerSoFarRow[columnIdx]
                currentCell = currentRow[columnIdx]
                if currentCell == 0 or currentCell == 1:
                    layerSoFarRow[columnIdx] = currentCell

    return layerSoFar

def printImage(decodedImage):
    for row in decodedImage:
        for cell in row:
            if cell == 0:
                print(" ", end='')
            elif cell == 1:
                print("*", end='')
        print()

printImage(decodeImage(assemble("0222112222120000", 2, 2), 2, 2))

with open('input.txt', 'r') as fp:
    line = fp.readline().rstrip()
    layers = assemble(line, 25, 6)
    print(solvePart1(layers))
    printImage(decodeImage(layers, 25, 6))
