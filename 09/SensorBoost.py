import sys
from functional import seq  # from PyFunctional

def allocateMoreMemory(memory, memoryPosition):
    while memoryPosition >= len(memory):
        memory.append(0)

def saveArg(memory, argMode, memoryPosition, relativeBase, valueToSave):
    if argMode == 0:
        allocateMoreMemory(memory, memoryPosition)
        outputPosn = memory[memoryPosition]
        allocateMoreMemory(memory, outputPosn)
        memory[outputPosn] = valueToSave
    elif argMode == 1:
        allocateMoreMemory(memory, memoryPosition)
        memory[memoryPosition] = valueToSave
    elif argMode == 2: # relative base
        allocateMoreMemory(memory, memoryPosition)
        adjustment = memory[memoryPosition]
        allocateMoreMemory(memory, adjustment + relativeBase)
        memory[adjustment + relativeBase] = valueToSave
    else:
        raise Exception("saveArg: unexpected argMode " + str(argMode) + " " + str(memoryPosition) + " " + str(valueToSave))


def getArgValue(memory, argMode, memoryPosition, relativeBase):
    if argMode == 0:
        allocateMoreMemory(memory, memoryPosition)
        allocateMoreMemory(memory, memory[memoryPosition])
        return memory[memory[memoryPosition]]
    elif argMode == 1:
        allocateMoreMemory(memory, memoryPosition)
        return memory[memoryPosition]
    elif argMode == 2:
        allocateMoreMemory(memory, memoryPosition)
        adjustment = memory[memoryPosition]
        allocateMoreMemory(memory, adjustment + relativeBase)
        return memory[adjustment + relativeBase]
    else:
        raise Exception("getArgValue: unexpected argMode " + str(argMode) + " " + str(memoryPosition))


def runProgram(memory, inputFromUser, startingPosition=0):
    currentPosition = startingPosition
    relativeBase = 0
    inputPosition = 0
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
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1, relativeBase)
            secondArgVal = getArgValue(memory, secondArgMode, currentPosition + 2, relativeBase)

            if currentOpCode == 1:
                opCodeResult = firstArgVal + secondArgVal
            elif currentOpCode == 2:
                opCodeResult = firstArgVal * secondArgVal

            saveArg(memory, thirdArgMode, currentPosition + 3, relativeBase, opCodeResult)
            currentPosition = currentPosition + 4

        # get input
        elif currentOpCode == 3:
            if inputPosition >= len(inputFromUser):
                raise Exception("ran out of user input: " + str(inputPosition) + " " + str(inputFromUser))
            currentInput = inputFromUser[inputPosition]
            saveArg(memory, firstArgMode, currentPosition + 1, relativeBase, currentInput)
            currentPosition = currentPosition + 2
            inputPosition = inputPosition + 1

        # print
        elif currentOpCode == 4:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1, relativeBase)
            currentPosition = currentPosition + 2
            print(firstArgVal)

        # jump if
        elif currentOpCode == 5 or currentOpCode == 6:
            conditional = getArgValue(memory, firstArgMode, currentPosition + 1, relativeBase)
            whereToJump = getArgValue(memory, secondArgMode, currentPosition + 2, relativeBase)
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
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1, relativeBase)
            secondArgVal = getArgValue(memory, secondArgMode, currentPosition + 2, relativeBase)
            valToSave = 0
            # less than
            if currentOpCode == 7 and firstArgVal < secondArgVal:
                valToSave = 1
            # equals
            elif currentOpCode == 8 and firstArgVal == secondArgVal:
                valToSave = 1
            saveArg(memory, thirdArgMode, currentPosition + 3, relativeBase, valToSave)
            currentPosition = currentPosition + 4

        elif currentOpCode == 9:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1, relativeBase)
            currentPosition = currentPosition + 2
            relativeBase = relativeBase + firstArgVal

        # unrecognized
        else:
            raise Exception(str(currentOpCode) + " is not recognized")

    return "DONE", 0


def parseMemoryFromStr(programStr):
    return (seq(programStr.split(","))
            .map(lambda token: token.rstrip())
            .map(lambda token: int(token))
            .to_list())

def solvePart1(programStr, input):
    runProgram(parseMemoryFromStr(programStr), input)

try:
    print("takes no input and produces a copy of itself as output")
    #  0 109,1,            increment relative base by 1
    #  2 204,-1,           print -1 relative to base
    #  4 1001,100,1,100,   add addr 100 and value 1 and save in addr 100
    #  8 1008,100,16,101,  equals addr 100 and 16, put 1 into addr 101
    # 12 1006,101,0,       jump to 0 if addr 101  is 0
    # 15 99                halt
    solvePart1("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", [])
    print("should output a 16-digit number")
    solvePart1("1102,34915192,34915192,7,4,7,99,0", [])
    print("should output 1125899906842624")
    solvePart1("104,1125899906842624,99", [])
except Exception as e:
    print(str(e))

with open('input.txt', 'r') as fp:
    line = fp.readline().rstrip()
    print("Part 1")
    solvePart1(line, [1])
