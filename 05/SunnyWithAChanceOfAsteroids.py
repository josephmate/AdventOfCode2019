import sys
from functional import seq  # from PyFunctional


def saveArg(memory, argMode, memoryPosition, valueToSave):
    if memoryPosition >= len(memory):
        raise Exception("saveArg: index out of bounds " + str(argMode) + " " + str(memoryPosition) + " " + str(len(memory)))
    if argMode == 0:
        outputPosn = memory[memoryPosition]
        if outputPosn >= len(memory):
            raise Exception("saveArg: index out of bounds " + str(argMode) + " " + str(memoryPosition) + " " + str(outputPosn) + " " + str(len(memory)))
        memory[outputPosn] = valueToSave
    elif argMode == 1:
        memory[memoryPosition] = valueToSave
    else:
        raise Exception("saveArg: unexpected argMode " + str(argMode) + " " + str(memoryPosition) + " " + str(valueToSave))


def getArgValue(memory, argMode, memoryPosition):
    if memoryPosition >= len(memory):
        raise Exception("getArgValue: index out of bounds " + str(argMode) + " " + str(memoryPosition) + " " + str(len(memory)))
    if argMode == 0:
        if memory[memoryPosition] >= len(memory):
            raise Exception("getArgValue: index out of bounds " + str(argMode) + " " + str(memoryPosition) + " " + str(memory[memoryPosition]) + " " + str(len(memory)))
        return memory[memory[memoryPosition]]
    elif argMode == 1:
        return memory[memoryPosition]
    else:
        raise Exception("getArgValue: unexpected argMode " + str(argMode) + " " + str(memoryPosition))


def runProgram(memory, inputFromUser):
    currentPosition = 0
    while True:
        if currentPosition >= len(memory):
            raise Exception("ran out of memory. unexpected currentPosition " + str(currentPosition) + " len" + str(len(memory)))

        encodedOpCode = memory[currentPosition]
        # ABCDE
        #  1002
        #
        # DE - two-digit opcode,      02 == opcode 2
        #  C - mode of 1st parameter,  0 == position mode
        #  B - mode of 2nd parameter,  1 == immediate mode
        #  A - mode of 3rd parameter,  0 == position mode,
        #                                   omitted due to being a leading zero
        currentOpCode = encodedOpCode % 100  # get last two digits
        firstArgMode = (encodedOpCode // 100) % 10  # get 3rd digit
        secondArgMode = (encodedOpCode // 1000) % 10  # get 4th digit
        thirdArgMode = (encodedOpCode // 10000) % 10  # get 5th digit

        # exit
        if currentOpCode == 99:
            break

        # add or multiply
        if currentOpCode == 1 or currentOpCode == 2:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1)
            secondArgVal = getArgValue(memory, secondArgMode, currentPosition + 2)

            if currentOpCode == 1:
                opCodeResult = firstArgVal + secondArgVal
            elif currentOpCode == 2:
                opCodeResult = firstArgVal * secondArgVal

            saveArg(memory, thirdArgMode, currentPosition + 3, opCodeResult)
            currentPosition = currentPosition + 4

        # get input
        elif currentOpCode == 3:
            saveArg(memory, firstArgMode, currentPosition + 1, inputFromUser)
            currentPosition = currentPosition + 2

        # print
        elif currentOpCode == 4:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1)
            print(firstArgVal)
            currentPosition = currentPosition + 2

        # jump if
        elif currentOpCode == 5 or currentOpCode == 6:
            conditional = getArgValue(memory, firstArgMode, currentPosition + 1)
            whereToJump = getArgValue(memory, secondArgMode, currentPosition + 2)
            # jump-if-true (jump-if-non-zero)
            if currentOpCode == 5 and conditional != 0:
                currentPosition = whereToJump
            # jump-if-false (jump-if-zero)
            elif currentOpCode == 6 and conditional == 0:
                currentPosition = whereToJump
            else:
                currentPosition = currentPosition + 3

        # comparison
        elif currentOpCode == 7 or currentOpCode == 8:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1)
            secondArgVal = getArgValue(memory, secondArgMode, currentPosition + 2)
            valToSave = 0
            # less than
            if currentOpCode == 7 and firstArgVal < secondArgVal:
                valToSave = 1
            # equals
            elif currentOpCode == 8 and firstArgVal == secondArgVal:
                valToSave = 1
            saveArg(memory, thirdArgMode, currentPosition + 3, valToSave)
            currentPosition = currentPosition + 4

        # unrecognized
        else:
            raise Exception(str(currentOpCode) + " is not recognized")

    return memory


def parseMemoryFromStr(programStr):
    return (seq(programStr.split(","))
            .map(lambda token: token.rstrip())
            .map(lambda token: int(token))
            .to_list())


def runProgramFromString(programStr, inputFromUser):
    return runProgram(parseMemoryFromStr(programStr), inputFromUser)

try:
    # test input instruction
    print("3,5,4,5,99,0 should print 1")
    print(str(runProgramFromString("3,5,4,5,99,0", 1)))

    # test all parameter mode instructions
    print("1,7,8,5,104,0,99,7,8 should print 4")
    print(str(runProgramFromString("1,7,8,5,104,0,99,1,3", 1)))
    print("101,7,8,5,104,0,99,1,2 should print 10")
    print(str(runProgramFromString("101,7,8,5,104,0,99,1,3", 1)))
    print("101,7,8,5,104,0,99,1,2 should print 9")
    print(str(runProgramFromString("1001,7,8,5,104,0,99,1,3", 1)))
    print("101,7,8,5,104,0,99,1,2 should print 4")
    print(str(runProgramFromString("10001,7,8,5,4,3,99,1,3", 1)))

    # test jump
    print("should print 100")
    print(str(runProgramFromString("5,9,10,104,100,99,104,1000,99,0,6", 1)))
    print("should print 1000")
    print(str(runProgramFromString("5,9,10,104,100,99,104,1000,99,1,6", 1)))


    # test comparison

except Exception as e:
    print(str(e))

with open('input.txt', 'r') as fp:
    line = fp.readline()
    print("Part 1")
    print(str(runProgramFromString(line, 1)))
    print("Part 2")
    print(str(runProgramFromString(line, 5)))
