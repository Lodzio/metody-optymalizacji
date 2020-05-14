import numpy as np
import functools
TAU = (np.sqrt(5) - 1) / 2
def goldenSectionSearch(fun, a, b, searchVector, epsilon):
    if (b - a) < epsilon:
        return np.mean([a, b])
    left = a + (1 - TAU) * (b - a)
    right = b - (1 - TAU) * (b - a)
    substitution = list(set(fun.variables()) - set(var[0] for var in searchVector))
    parameters = {var: val for var, val in searchVector}
    parametersValue = [{**parameters, substitution[0]: side} for side in (left, right)]

    if fun.evaluate(parametersValue[0]) < fun.evaluate(parametersValue[1]):
        return goldenSectionSearch(fun, a, right, searchVector, epsilon)
    else:
        return goldenSectionSearch(fun, left, b, searchVector, epsilon)
