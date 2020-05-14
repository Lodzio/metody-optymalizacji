import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def count_function_value(parser_fun, *args):
    eval_dict = dict(zip(parser_fun.variables(), args))
    return parser_fun.evaluate(eval_dict)


def plot_path_graph(gs_object, graph_3d=False):
    vec_fun = np.vectorize(count_function_value)
    points = []
    gauss_steps = gs_object.path
    bounds = []
    for i in range(2):
        axis_bound = sorted([fun(gauss_steps, key=lambda t: t[i])[i] for fun in (min, max)])
        bounds.append(axis_bound)
    for axis in bounds:
        points.append(np.linspace(axis[0] - 3, axis[1] + 3, 300))

    mesh = np.meshgrid(*points)
    height = vec_fun(gs_object.fun, *mesh)

    if not graph_3d:
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(*mesh, height, 60)
        fig.colorbar(cp)

        x = [np.linspace(gauss_steps[i][0], gauss_steps[i + 1][0], 2) for i in range(len(gauss_steps) - 1)]
        y = [np.linspace(gauss_steps[i][1], gauss_steps[i + 1][1], 2) for i in range(len(gauss_steps) - 1)]
        plt.plot(x, y, color="orangered")
    else:
        x = [gauss_step[0] for gauss_step in gauss_steps]
        y = [gauss_step[1] for gauss_step in gauss_steps]
        z = vec_fun(gs_object.fun, x, y)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(*mesh, height, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, alpha=.5)
        ax.plot(x, y, z, color="orangered")

    plt.show()

