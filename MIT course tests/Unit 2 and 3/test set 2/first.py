"""
Goal:
Write a program to calculate the credit card balance after one year
if a person only pays the minimum monthly payment
required by the credit card company each month.

For each month, calculate statements on the monthly payment and remaining balance.
At the end of 12 months, print out the remaining balance.
Be sure to print out no more than two decimal digits of accuracy

Variables
balance - the outstanding balance on the credit card
annualInterestRate - annual interest rate as a decimal
monthlyPaymentRate - minimum monthly payment rate as a decimal

The code you paste into the following box should not specify the values for the variables
balance, annualInterestRate, or monthlyPaymentRate

A summary of the required math is found below:
    Monthly interest rate= (Annual interest rate) / 12.0
    Minimum monthly payment = (Minimum monthly payment rate) x (Previous balance)
    Monthly unpaid balance = (Previous balance) - (Minimum monthly payment)
    Updated balance each month = (Monthly unpaid balance) + (Monthly interest rate x Monthly unpaid balance)


# Test case 1
    balance = 42
    annualInterestRate = 0.2
    monthlyPaymentRate = 0.04

    # Result Your Code Should Generate Below:
    Remaining balance: 31.38

# Test case 2
    balance = 484
    annualInterestRate = 0.2
    monthlyPaymentRate = 0.04

    Result Your Code Should Generate Below:
    Remaining balance: 361.61
"""
balance = 484
annualInterestRate = 0.2
monthlyPaymentRate = 0.04

i = 1
while i < 13:
    min_payment = monthlyPaymentRate * balance
    outstanding = balance - min_payment
    balance = outstanding * (1. + annualInterestRate / 12.)   # outstanding balance + interest due
    i += 1

# print(f"Remaining balance: {balance: .2f}")
print("Remaining balance:", round(balance, 2))
