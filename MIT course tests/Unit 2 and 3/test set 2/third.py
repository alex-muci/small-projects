"""
Improve - by getting much faster for large amounts - using Bisection search to the last cent

Bounds:
    Monthly interest rate = (Annual interest rate) / 12.0
    Monthly payment lower bound = Balance / 12
    Monthly payment upper bound = (Balance x (1 + Monthly interest rate)12) / 12.0

Test Case 1:
    balance = 320000
    annualInterestRate = 0.2

    Result Your Code Should Generate:
    -------------------
    Lowest Payment: 29157.09

Test Case 2:
    balance = 999999
    annualInterestRate = 0.18

    Result Your Code Should Generate:
    -------------------
    Lowest Payment: 90325.03
"""

balance = 999999
annualInterestRate = 0.18


# define bounds (implicit assuming that rates are positive)
monthly_int_rate = annualInterestRate / 12.
montly_lower_bound = balance / 12.
montly_upper_bound = balance * (1 + monthly_int_rate)**12 / 12.


def final_balance(monthly_payment,
                  _balance=balance, _monthly_int_rate=monthly_int_rate):
    for i in range(1, 13):
        outstanding = _balance - monthly_payment
        _balance = outstanding * (1. + _monthly_int_rate)  # outstanding balance + interest due
    return _balance


def find_value_bisection(fun, low, up,
                         max_iters=1000, tol=0.01):
    # check that it is monotonic, i.e. value in mid-point
    if fun(low) * fun(up) >= 0:
        raise Exception("Cannot find result with Bisection: function is not monotonic!")

    num_iter, low_n, up_n = 1, low, up  # initialise here
    while num_iter < max_iters:
        mid_point = (low_n + up_n) / 2.
        fun_mid_point = fun(mid_point)

        if up_n - low_n < tol * 2.:
            return mid_point

        num_iter += 1
        fun_low_n = fun(low_n)

        if fun_low_n * fun_mid_point > 0:  # i.e. same sign
            low_n = mid_point
        else:
            up_n = mid_point

    raise Exception("Cannot find result with Bisection: max number of iterations reached!")


result = find_value_bisection(final_balance, montly_lower_bound, montly_upper_bound)
print("Lowest Payment: {:.2f}".format(result))
