import numpy as np
import functools
import math

TAU = (np.sqrt(5) - 1) / 2
def goldenSectionSearch(variables, fun, a, b, epsilon):
    if np.linalg.norm(b - a) < epsilon:
        return (a + b) / 2
    left = a + ((1 - TAU) * (b - a))
    right = b - ((1 - TAU) * (b - a))
    leftVal = fun(dict(zip(variables, left)))
    rightVal = fun(dict(zip(variables, right)))
    if leftVal < rightVal:
        return goldenSectionSearch(variables, fun, a, right, epsilon)
    else:
        return goldenSectionSearch(variables, fun, left, b, epsilon)
