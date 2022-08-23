import itertools


def how_many(aDict):
    '''
    aDict: A dictionary, where all the values are lists.

    returns: int, how many values are in the dictionary (flattening values that are list).
    '''
    merged = list(itertools.chain(*list(aDict.values())))
    return len(merged)


def biggest(aDict):
    '''
    aDict: A dictionary, where all the values are lists.

    returns: The key with the largest number of values associated with it
    '''
    if not aDict:
        return None

    so_far = 0
    for k, v, in aDict.items():
        if len(v) > so_far:
            sofar, biggest_key_so_far = len(v), k

    return biggest_key_so_far


#   #   #   #   #   #   #   #   #   #
def fib(x):
    """ Fibonacci """
    # global numFibCalls
    # numFibCalls += 1
    if x == 0 or x == 1:  # NB: we need to base cases
        return 1
    else:
        return fib(x-1) + fib(x-2)

def fib2(n, d=None):
    """ a much more efficient Fibonacci using dict (memoization)
        e.g. n=34 generates just 57 calls for fib2 vs. over 11 million for for fib!
    """
    # global numFibCalls
    # numFibCalls += 1
    d = {1: 1, 2: 2} if d is None else d  # base cases as default

    if n in d:  # if already computed, just look it up  --- of course better using lru_cache
        return d[n]
    else:
        res = fib2(n-1, d) + fib2(n-2, d)
        d[n] = res  # storing
        return res


#   #   #   #   #   #   #   #   #   #
def uniqueValues(aDict):
    """
    Write a Python function that returns a list of keys in aDict that map
    to integer values that are unique (i.e. values appear exactly once in aDict).
    The list of keys you return should be sorted in increasing order.
    (If aDict does not contain any unique values, you should return an empty list.)
    """

    keep, already_seen = {}, set()
    for k, v in aDict.items():
        if v in already_seen:
            if v in keep:      # remove it, we have already see this
                del keep[v]
        else:                  # add it for now and store the key, keep track of what seen
            keep[v] = k
            already_seen.add(v)

    lista = list(keep.values())

    return sorted(lista)


#   #   #   #   #   #   #   #   #   #
if __name__ == "__main__":

    import time

    print(how_many({'b': [1, 7, 5, 4, 3, 18, 10, 0], 'a': []}))
    print(biggest({'b': [1, 7, 5, 4, 3, 18, 10, 0], 'a': []}))

    num = 35
    numFibCalls = 0

    d = {1: 1, 2: 2}  #  base cases as default
    start = time.time()
    print(fib2(num, d))
    print(f"running in {time.time() - start:.2f} secs.")
    # print(numFibCalls)

    numFibCalls = 0
    start = time.time()
    print(fib(num))
    print(f"running in {time.time() - start:.2f} secs.")
