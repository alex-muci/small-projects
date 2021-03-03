"""
Now write a program that calculates the minimum fixed monthly payment needed in order pay off a credit card balance
within 12 months. By a fixed monthly payment, we mean a single number which does not change each month,
but instead is a constant amount that will be paid each month.

In this problem, we will not be dealing with a minimum monthly payment rate.
The following variables contain values as described below:
    balance - the outstanding balance on the credit card
    annualInterestRate - annual interest rate as a decimal

The program should print out one line: the lowest monthly payment that will pay off all debt in under 1 year,
for example:
Lowest Payment: 180

Assume that the interest is compounded monthly according to the balance at the end of the month
(after the payment for that month is made).

> The monthly payment must be a multiple of $10 and is the same for all months.

Test Case 1:
    balance = 3329
    annualInterestRate = 0.2

    Result Your Code Should Generate:
    -------------------
    Lowest Payment: 310

Test Case 2:
    balance = 4773
    annualInterestRate = 0.2

    Result Your Code Should Generate:
    -------------------
    Lowest Payment: 440
"""

balance = 4773
annualInterestRate = 0.2


# NB: this asks for a brute force approach since using multiple of 10 (next problem is with bisection)
# so no need to b

def final_balance(balance, lowest_payment, annualInterestRate):
    for i in range(1, 13):
        outstanding = balance - lowest_payment
        balance = outstanding * (1. + annualInterestRate / 12.)  # outstanding balance + interest due
    return balance


lowest_payment = max(10, int((balance / 12 - 5) // 10) * 10)  # lowest multiple of 10 closer to balance/12 (round down)
while final_balance(balance, lowest_payment, annualInterestRate) > 0:
    lowest_payment += 10

print("Lowest Payment: {}".format(lowest_payment))
