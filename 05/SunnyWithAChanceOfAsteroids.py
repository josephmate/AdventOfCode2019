import sys
from functional import seq  # from PyFunctional


def runProgram(memory):
    currentPosition = 0
    while True:
        currentOpCode = memory[currentPosition]
        if currentOpCode == 99:
            break

        firstArgPosn = memory[currentPosition + 1]
        secondArgPosn = memory[currentPosition + 2]
        outputPosn = memory[currentPosition + 3]
        if currentOpCode == 1:
            # additions
            memory[outputPosn] = memory[firstArgPosn] + memory[secondArgPosn]
        elif currentOpCode == 2:
            # multiplication
            memory[outputPosn] = memory[firstArgPosn] * memory[secondArgPosn]
        else:
            raise Exception(str(currentOpCode) + " is not recognized")
        currentPosition = currentPosition + 4

    return memory


inputMemory = (seq(sys.stdin.readline().split(','))
               .map(lambda token: token.rstrip())
               .map(lambda token: int(token))
               ).to_list()

part1Memory = inputMemory.copy()
# replace position 1 with the value 12
part1Memory[1] = 12
# and replace position 2 with the value 2.
part1Memory[2] = 2
runProgram(part1Memory)
print(str(part1Memory[0]))

# Each of the two input values will be between 0 and 99, inclusive.
for noun in range(0, 100):
    # Each of the two input values will be between 0 and 99, inclusive.
    for verb in range(0, 100):
        part2Memory = inputMemory.copy()
        # The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before.
        # In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb.
        part2Memory[1] = noun
        part2Memory[2] = verb
        runProgram(part2Memory)
        # Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.
        # Find the input noun and verb that cause the program to produce the output 19690720.
        if part2Memory[0] == 19690720:
            # What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)
            print(str(100 * noun + verb))
