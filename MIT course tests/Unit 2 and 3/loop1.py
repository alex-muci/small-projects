iteration = 0
while iteration < 5:
    count = 0
    for letter in "hello, world":
        count += 1
        if iteration % 2 == 0:
            break
    print("Iteration " + str(iteration) + "; count is: " + str(count))
    iteration += 1


#   #   #   #   #   #   #   #   #   #   #   #   #   #
def f(s):
    return 'a' in s


def satisfiesF(L):
    """
    Assumes L is a list of strings
    Assume function f is already defined for you and it maps a string to a Boolean
    Mutates L such that it contains all of the strings, s, originally in L such
            that f(s) returns True, and no other elements. Remaining elements in L
            should be in the same order.
    Returns the length of L after mutation
    """
    idx =0
    while idx < len(L):
        if f(L[idx]):  # do nothing if f true
            idx += 1
        else:       # remove the element if false
            L.pop(idx)

    return len(L)


#   #   #   #   #   #   #   #   #   #   #   #   #   #
if __name__ == "__main__":

    L = ['a', 'b', 'a', 'c', 'c', 'd', 'h', 'a']
    print(satisfiesF(L))
    print(L)
