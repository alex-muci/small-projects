"""
Recursion may be more efficient from a programmer's point of view (more intuitive),
but may not be for a computer!
"""

# multiplication by iteration
def mult_iter(a, b):
    result = 0
    while b > 0:
        result += a
        b -= 1
    return result


# multiplication by recursion
def mult_recur(a, b):
    if b == 1:    # base case, always
        return a
    else:
        return a + mult_recur(a, b-1)


# classical example of recursion: factorial
def fact(n):
    if n == 0:
        return 1
    return n * fact(n-1)

def fact_iter(n):
    p = 1
    for i in range(1, n+1):
        p *= i
    return p


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def iterPower(base, exp):
    """
    base: int or float.
    exp: int >= 0

    returns: int or float, base^exp
    """
    res = 1  # <---- remember starting point
    while exp > 0:
        res *= base
        exp -= 1
    return res


def recurPower(base, exp):
    if exp == 0:
        return 1
    return base * recurPower(base, exp - 1)


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def gcd_recur(a, b):
    """
    Euclide's trick to calculate gcd: perfect for applying recursion

    a, b: positive integers
    returns: a positive integer, the greatest common divisor of a & b.
    """
    if b == 0:
        return a
    else:
        return gcd_recur(b, a % b)


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def fib(x):
    """ Fibonacci """
    if x == 0 or x == 1:  # NB: we need to base cases
        return 1
    else:
        return fib(x-1) + fib(x-2)


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def is_palindrome(s):
    import string

    def to_chars(s):
        s = s.lower()
        ans = ''
        for c in s:
            if c in string.ascii_lowercase:  # or just the string of letters
                ans = ans + c
            return ans

    def is_pal(s):
        if len(s) <= 1:
            return True
        else:
            return s[0] == s[-1] and is_pal(s[1:-1])

    return is_pal(to_chars(s))


#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
# Towers of Hanoi
def towers(n, fr, to, spare):
    if n == 1:
        print('move from ' + str(fr) + ' to ' + str(to))
    else:
        towers(n-1, fr, spare, to)
        towers(1, fr, to, spare)
        towers(n-1, spare, to, fr)


#   #   #   #   #   #   #   #   #   #
if __name__ == "__main__":

    a, b = 5, 7

    print(mult_iter(a, b))
    print(mult_recur(a, b))

    print(fact(4))  # 1*2*3*4 = 24
    print(fact_iter(4))

    print(towers(4, 'P1', 'P2', 'P3'))

    print(fib(2))
