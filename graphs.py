import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def getFuntionResult(parser_fun, *args):
    parameters = dict(zip(parser_fun.variables(), args))
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
    height = vec_fun(searchAlgorithm.fun, *mesh)
    fig, ax = plt.subplots(1, 1)
    cp = ax.contourf(*mesh, height, 60)
    fig.colorbar(cp)

    x = [np.linspace(path[i][0], path[i + 1][0], 2) for i in range(len(path) - 1)]
    y = [np.linspace(path[i][1], path[i + 1][1], 2) for i in range(len(path) - 1)]
    plt.plot(x, y, color="orangered")

    plt.show()

