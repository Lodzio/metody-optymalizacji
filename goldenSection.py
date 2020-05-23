import numpy as np
import functools
import math

TAU = (np.sqrt(5) - 1) / 2
def goldenSectionSearch(fun, a, b, epsilon):
    if np.linalg.norm(b - a) < epsilon:
        return (a + b) / 2
    left = a + (1 - TAU) * (b - a)
    right = b - (1 - TAU) * (b - a)
    # substitution = list(set(fun.variables()) - set(var[0] for var in searchVector))
    # parameters = {var: val for var, val in searchVector}
    # parametersValue = [{**parameters, substitution[0]: side} for side in (left, right)]
    leftVal = fun({"x1": left[0], "x2": left[1]})
    rightVal = fun({"x1": right[0], "x2": right[1]})
    if leftVal < rightVal:
        return goldenSectionSearch(fun, a, right, epsilon)
    else:
        return goldenSectionSearch(fun, left, b, epsilon)
