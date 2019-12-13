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


def runProgram(memory, inputFromUser, startingPosition=0):
    currentPosition = startingPosition
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
            if inputPosition >= len(inputFromUser):
                raise Exception("ran out of user input: " + str(inputPosition) + " " + str(inputFromUser))
            currentInput = inputFromUser[inputPosition]
            saveArg(memory, firstArgMode, currentPosition + 1, currentInput)
            currentPosition = currentPosition + 2
            inputPosition = inputPosition + 1

        # print
        elif currentOpCode == 4:
            firstArgVal = getArgValue(memory, firstArgMode, currentPosition + 1)
            currentPosition = currentPosition + 2
            return firstArgVal, currentPosition

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

    return "DONE", 0


def parseMemoryFromStr(programStr):
    return (seq(programStr.split(","))
            .map(lambda token: token.rstrip())
            .map(lambda token: int(token))
            .to_list())

def permutationImpl(permutationSet, permutationSoFar):
    if len(permutationSet) == 0:
        return [permutationSoFar.copy()]

    result = []
    for entry in permutationSet.copy():
        permutationSet.remove(entry)
        permutationSoFar.append(entry)
        result = result + permutationImpl(permutationSet, permutationSoFar)
        permutationSoFar.pop()
        permutationSet.add(entry)

    return result

def permutations(listToPermutate):
    permuatationSet = set()
    for item in listToPermutate:
        permuatationSet.add(item)
    return permutationImpl(permuatationSet, [])

def solve(programString):
    originalMemory = parseMemoryFromStr(programString)
    allPhaseSettingSequences = permutations([0, 1, 2, 3, 4])
    maxSoFar = 0
    for permutation in allPhaseSettingSequences:
        previousResult = 0
        for phaseSetting in permutation:
            (previousResult, currentPosition) = runProgram(originalMemory.copy(), [phaseSetting, previousResult])

        if previousResult > maxSoFar:
            maxSoFar = previousResult

    return maxSoFar


def runUntilCompletion(permutation, originalMemory):
    phaseMemory = []
    instructionPointers = []

    previousResult = 0
    for idx in range(0, 5):
        phaseMemory.append(originalMemory.copy())
        phaseSetting = permutation[idx]
        (previousResult, instructionPointer) = runProgram(phaseMemory[idx], [phaseSetting, previousResult])
        instructionPointers.append(instructionPointer)

    while True:
        for idx in range(0, 5):
            (currentResult, instructionPointer) = runProgram(phaseMemory[idx], [previousResult], instructionPointers[idx])
            if currentResult == "DONE":
                return previousResult
            previousResult = currentResult
            instructionPointers[idx] = instructionPointer


def solvePart2(programString):
    originalMemory = parseMemoryFromStr(programString)
    allPhaseSettingSequences = permutations([5, 6, 7, 8, 9])
    maxSoFar = 0
    for permutation in allPhaseSettingSequences:
        outputSignal = runUntilCompletion(permutation, originalMemory)
        if outputSignal > maxSoFar:
            maxSoFar = outputSignal

    return maxSoFar


try:
    print("should print 43210")
    print(str(solve("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")))
    print("should print 54321")
    print(str(solve("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")))
    print("should print 65210")
    print(str(solve("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")))

    print("Part 2 tests")
    print("should print 139629729")
    #  0  3,26,               read and save to addr 26
    #  2  1001,26,-4,26,      add addr 26 with -4 and save in addr 26
    #  6  3,27,               read and save to addr 27
    #  8  1002,27,2,27,       multiply addr 27 with 2 and save in addr 27
    # 12  1,27,26,27,         add addr 27 addr 26 and save to addr 27
    # 16  4,27,               output addr 27
    # 18  1001,28,-1,28,      add addr 28 and value -1 and save to addr 28
    # 22  1005,28,6,          jump if addr 28 is not 0, jump to 6
    # 25  99,
    # 26  0,0,5
    print(str(solvePart2("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")))
    print("should print 18216")
    #  0  3,52,
    #  2  1001,52,-5,52,
    #  6  3,53,
    #  8  1,52,56,54,
    # 12  1007,54,5,55,
    # 16  1005,55,26,
    # 20  1001,54,-5,54,
    # 24  1105,1,12,
    # 27  1,53,54,53,
    # 31  1008,54,0,55,
    # 35  1001,55,1,55,
    # 39  2,53,55,53,
    # 43  4,53,
    # 45  1001,56,-1,56,
    # 49  1005,56,6,
    # 52  99,
    # 53  0,0,0,0,10
    print(str(solvePart2("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")))
except Exception as e:
    print(str(e))

with open('input.txt', 'r') as fp:
    line = fp.readline()
    print("Part 1")
    print(str(solve(line)))
    print("Part 2")
    print(str(solvePart2(line)))
