import math
import matplotlib.pyplot as plt
from functools import reduce

from typing import List, Tuple, Callable

Vector = List[float]

def vector_add(v: Vector, w: Vector) -> Vector:
    assert len(v) == len(w)
    return [vi + wi for vi, wi in zip(v, w)]

assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]
