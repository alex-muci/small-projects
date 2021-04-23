"""
def isPalindrome(aString):
    '''
    aString: a string
    '''
    # Your code here

    start, end = 0, len(aString) - 1
    while start < end:
        if aString[start].lower() != aString[end].lower():
            return False
        start += 1
        end -= 1
    return True

testfalse = 'ray a Ray'
testtrue = "able was I ere I saw Elba"

print(isPalindrome(testfalse))
print(isPalindrome(testtrue))
"""

"""
from collections import Counter

def is_list_permutation_2(L1, L2):
    '''
    L1 and L2: lists containing integers and strings
    Returns False if L1 and L2 are not permutations of each other.
            If they are permutations of each other, returns a
            tuple of 3 items in this order:
            the element occurring most, how many times it occurs, and its type
    '''
    if len(L1) != len(L2):
        return False

    # I am going to use Counter
    freqL1 = Counter(L1)
    freqL2 = Counter(L2)

    if freqL1 == freqL2:
        mostcommon = freqL1.most_common()[0]
        return (mostcommon[0], mostcommon[1], type(mostcommon[0]))

    return False



def is_list_permutation(L1, L2):
    '''
    L1 and L2: lists containing integers and strings
    Returns False if L1 and L2 are not permutations of each other.
            If they are permutations of each other, returns a
            tuple of 3 items in this order:
            the element occurring most, how many times it occurs, and its type
    '''
    if len(L1) != len(L2):
        return False

    if len(L1) == 0 and len(L2) == 0:
        return (None, None, None)

    def get_freq(s):
        res = {}
        for l in s:
            res[l] = res.get(l, 0) + 1
        return res

    freqL1 = get_freq(L1)
    freqL2 = get_freq(L2)

    if freqL1 == freqL2:
        mostcommon = sorted(freqL1.items(), key=lambda item: item[1], reverse=True)[0]
        return (mostcommon[0], mostcommon[1], type(mostcommon[0]))

    return False


L1 = ['a', 'a', 'b']; L2 = ['a', 'b']  # then is_list_permutation returns False
L11 = [1, 'b', 1, 'c', 'c', 1]; L22 = ['c', 1, 'b', 1, 1, 'c'] # then is_list_permutation returns (1, 3, <class 'int'>) because the integer 1 occurs the most, 3 times, and the type of 1 is an integer (note that the third element in the tuple is not a string).

print(is_list_permutation(L1, L2))
print(is_list_permutation(L11, L22))
print(is_list_permutation([], []))  # (None, None, None)

print(is_list_permutation([1, 2, 1], [2, 1, 2]))   # False

"""
"""
def uniqueValues(aDict):
    '''
    aDict: a dictionary
    returns: a sorted list of keys that map to unique aDict values, empty list if none
    '''

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




aDict1 = {1: 1, 3: 2, 6: 0, 7: 0, 8: 4, 10: 0} # then your function should return [1, 3, 8]
aDict2 = {1: 1, 2: 1, 3: 1}  # then your function should return []

print(uniqueValues(aDict1))
print(uniqueValues(aDict2))
print(uniqueValues({}))
"""

"""
## DO NOT MODIFY THE IMPLEMENTATION OF THE Person CLASS ##
class Person(object):
    def __init__(self, name):
        # create a person with name name
        self.name = name
        try:
            firstBlank = name.rindex(' ')
            self.lastName = name[firstBlank + 1:]
        except:
            self.lastName = name
        self.age = None

    def getLastName(self):
        # return self's last name
        return self.lastName

    def setAge(self, age):
        # assumes age is an int greater than 0
        # sets self's age to age (in years)
        self.age = age

    def getAge(self):
        # assumes that self's age has been set
        # returns self's current age in years
        if self.age == None:
            raise ValueError
        return self.age

    def __lt__(self, other):
        # return True if self's name is lexicographically less
        # than other's name, and False otherwise
        if self.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName

    def __str__(self):
        # return self's name
        return self.name


class USResident(Person):
    '''
    A Person who resides in the US.
    '''
    def __init__(self, name, status):
        '''
        Initializes a Person object. A USResident object inherits
        from Person and has one additional attribute:
        status: a string, one of "citizen", "legal_resident", "illegal_resident"
        Raises a ValueError if status is not one of those 3 strings
        '''
        super().__init__(name)
        if status not in ("citizen", "legal_resident", "illegal_resident"):
            raise ValueError("not a good status")
        self.status = status

    def getStatus(self):
        '''
        Returns the status
        '''
        return self.status
"""


class myDict(object):
    """ Implements a dictionary without using a dictionary """

    def __init__(self):
        """ initialization of your representation """
        self.key, self.v = [], []

    def assign(self, k, v):
        """ k (the key) and v (the value), immutable objects  """
        try:  #  see if exists already
            idx = self.key.index(k)
            self.v[idx] = v
        except:
            self.key.append(k)
            self.v.append(v)


    def getval(self, k):
        """ k, immutable object  """
        try:
            idx = self.key.index(k)
        except:
            raise KeyError("Key does not exist")
        else:
            return self.v[idx]

    def delete(self, k):
        """ k, immutable object """
        idx = self.key.index(k)
        del self.v[idx]
        self.key.remove(k)


"""
With a dict:       With a myDict:
-------------------------------------------------------------------------------
d = {}             md = myDict()        # initialize a new object using 
                                          your choice of implementation

d[1] = 2           md.assign(1,2)       # use assign method to add a key,value pair

print(d[1])        print(md.getval(1))  # use getval method to get value stored for key 1

del(d[1])          md.delete(1)         # use delete method to remove 
                                          key,value pair associated with key 1
"""
md = myDict()
md.assign(1, 2)
print(md.getval(1))
md.assign(1, 3)
print(md.getval(1))
md.assign(2, 5)
md.delete(1)
print(md.getval(2))
print(md.getval(1))

d1 = md.myDict()
d1.assign(1, 2)
d1.delete(3)
