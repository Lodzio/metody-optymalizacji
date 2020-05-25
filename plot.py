import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def getFuntionResult(parser_fun, fun, *args):
    parameters = dict(zip(parser_fun.variables(), args))
    return 1/fun(parameters)
    return parser_fun.evaluate(parameters)


def plot(searchAlgorithm):
    vec_fun = np.vectorize(getFuntionResult)
    path = searchAlgorithm.path
    bounds = []
    meshPoints = []
    for i in range(2):
        axis_bound = sorted([fun(path, key=lambda t: t[i])[i] for fun in (min, max)])
        bounds.append(axis_bound)
    for axis in bounds:
        meshPoints.append(np.linspace(axis[0] - 3, axis[1] + 3, 300))

    mesh = np.meshgrid(*meshPoints)
    height = vec_fun(searchAlgorithm.fun, searchAlgorithm.getFunctionResult,*mesh)
    fig, ax = plt.subplots(1, 1)
    cp = ax.contourf(*mesh, height, 60)
    fig.colorbar(cp)

    x = [np.linspace(path[i][0], path[i + 1][0], 2) for i in range(len(path) - 1)]
    y = [np.linspace(path[i][1], path[i + 1][1], 2) for i in range(len(path) - 1)]
    for vector in searchAlgorithm.vectors:
        plt.plot([vector[0][0], vector[1][0]], [vector[0][1], vector[1][1]], color="blue")
    plt.plot(x, y, color="red")

    plt.show()

