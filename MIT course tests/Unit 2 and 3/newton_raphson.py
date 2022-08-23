"""
Newton-raphson: faster than bisection

use to find polinominal root, e.g. sqrt

 [better guess] = guess - [polynomial value of guess] / [derivative of polynomial at that guess]
"""

eps = 0.01
y = 64
guess = y / 2.
numGuesses = 0

while abs(guess * guess - y) >= eps:
    numGuesses += 1
    guess = guess - (guess**2 - y) / (2* guess)

print(f"numGuesses: {numGuesses}.")
print(f"Square root of {y} is about {guess}.")
