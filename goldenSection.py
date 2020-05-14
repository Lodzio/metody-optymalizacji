import numpy as np
import functools
TAU = (np.sqrt(5) - 1) / 2
def goldenSectionSearch(fun, a, b, constant, epsilon):
    if (b - a) < epsilon:
        return np.mean([a, b])
    left_x = a + (1 - TAU) * (b - a)
    right_x = b - (1 - TAU) * (b - a)
    substitution = list(set(fun.variables()) - set(var[0] for var in constant))
    eval_dict = {var: val for var, val in constant}
    fun_eval = [{**eval_dict, substitution[0]: side} for side in (left_x, right_x)]

    if fun.evaluate(fun_eval[0]) < fun.evaluate(fun_eval[1]):
        return goldenSectionSearch(fun, a, right_x, constant, epsilon=epsilon)
    else:
        return goldenSectionSearch(fun, left_x, b, constant, epsilon=epsilon)
