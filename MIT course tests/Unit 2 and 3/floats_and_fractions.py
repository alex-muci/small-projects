"""
Recall binary and decimal representation in terms of powers of 2 and 10 -
then easy to convert between the two (e.g. 10 decimal is 8 + 2 = 2^3+ 0 + 2^1 + 0 = 1010)

Fractions as binary:
 i. multiply by a power of 2 big enough to get an integer
ii. convert to binary
iii. divide it by the power of 2


example (nice number):
 3/8 = 0.375
 i. 0.3755 * 2**3 = 3 (decimal)
 ii 3 (decimal) = 11 (binary)
 iii. divide by 2**3 (shift right) to get 0.011 (binary)

but 0.1 = 0.0001100110011001101  because the binary is an approx
"""
x = float(input("Enter a decimal number between 0 and 1: "))

# # # # increase decimal to integer
p = 0
while ((2**p) * x) % 1 != 0:
    print("Reminder = " + str((2**p) * x - int((2**p) * x)))
    p += 1
num = int((2**p) * x)

# # # # this part is conversion from decimal integer to binary  # # # #
result = ""
if num == 0:
    result = '0'
while num > 0:
    result = str(num % 2) + result  # NB: position means this is a stack!
    num = num//2

# # # # put zeroes in front
for i in range(p - len(result)):
    result = '0' + result
result = result[0:-p] + '.' + result[-p:]

print('The binary representation of the decimal is ' + str(result))