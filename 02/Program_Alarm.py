import sys
from functional import seq  # from PyFunctional


def runProgram(opCodes):
    currentPosition = 0
    while True:
        currentOpCode = opCodes[currentPosition]
        print(str(opCodes))
        print(str(currentOpCode))
        if currentOpCode == 99:
            break

        firstArgPosn = opCodes[currentPosition + 1]
        secondArgPosn = opCodes[currentPosition + 2]
        outputPosn = opCodes[currentPosition + 3]
        if currentOpCode == 1:
            # additions
            opCodes[outputPosn] = opCodes[firstArgPosn] + opCodes[secondArgPosn]
        elif currentOpCode == 2:
            # multiplication
            opCodes[outputPosn] = opCodes[firstArgPosn] * opCodes[secondArgPosn]
        else:
            raise Exception(str(currentOpCode) + " is not recognized")
        currentPosition = currentPosition + 4

    return opCodes


opCodes = (seq(sys.stdin.readline().split(','))
           .map(lambda token: token.rstrip())
           .map(lambda token: int(token))
           ).to_list()

# before running the program,
# replace position 1 with the value 12
opCodes[1] = 12
# and replace position 2 with the value 2.
opCodes[2] = 2
# What value is left at position 0 after the program halts?
runProgram(opCodes)
print(str(opCodes))

