import sys
from functional import seq  # from PyFunctional


def countDigits(layer, digit):
    digitCount = 0
    for row in layer:
        for cell in row:
            if cell == digit:
                digitCount = digitCount + 1
    return digitCount


def solve(layers):
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
print(str(solve(assemble(inputSmall, smallWidth, smallHeight))))

with open('input.txt', 'r') as fp:
    line = fp.readline().rstrip()
    print(solve(assemble(line, 25, 6)))
