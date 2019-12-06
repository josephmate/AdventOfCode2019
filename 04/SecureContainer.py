def toDigits(number):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    digits.reverse()
    return digits


# Two adjacent digits are the same (like 22 in 122345).
def hasTwoSameAdjacentDigits(digits):
    previousDigit = 10
    for digit in digits:
        if digit == previousDigit:
            return True
        previousDigit = digit
    return False


# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
def digitsNeverDecrease(digits):
    previousDigit = -1
    for digit in digits:
        if digit < previousDigit:
            return False
        previousDigit = digit
    return True


def meetsCriteria(number):
    digits = toDigits(number)
    return hasTwoSameAdjacentDigits(digits) and digitsNeverDecrease(digits)


print(str(toDigits(123)))
print("digitsNeverDecrease(123): " + str(digitsNeverDecrease(toDigits(123))))
print("digitsNeverDecrease(321): " + str(digitsNeverDecrease(toDigits(321))))
print("digitsNeverDecrease(122): " + str(digitsNeverDecrease(toDigits(122))))
print("hasTwoSameAdjacentDigits(123): " + str(hasTwoSameAdjacentDigits(toDigits(123))))
print("hasTwoSameAdjacentDigits(122): " + str(hasTwoSameAdjacentDigits(toDigits(122))))
print("hasTwoSameAdjacentDigits(222): " + str(hasTwoSameAdjacentDigits(toDigits(222))))



numThatMeetCriteria = 0
for i in range(272091, 815432 + 1):
    if meetsCriteria(i):
        numThatMeetCriteria = numThatMeetCriteria + 1
print("Part 1:")
print(str(numThatMeetCriteria))
