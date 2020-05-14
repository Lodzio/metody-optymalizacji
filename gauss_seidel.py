import numpy as np
from py_expression_eval import Parser
from goldenSection import goldenSectionSearch
from graphs import plot_path_graph


class GaussSeidel:
    def __init__(self, fun, startPoint, oneStepSize=2, epsilon=10e-3, stepsLimit=3000):
        self.fun = fun
        self.fun_minimum = None
        self.epsilon = epsilon
        self.stepsLimit = stepsLimit
        self.oneStepSize = oneStepSize
        self.path = []
        self._positionIndex = 0
        self._stepNumber = 0
        self.currentPos = np.array(startPoint, dtype="float")
        self._variables = sorted(fun.variables())
        self.funValue = self.getFunctionValue()

    def __str__(self):
        strPoint = [str(round(axis, 3)) for axis in self.currentPos]
        repr_str = f"Step {self._stepNumber}: Point - [{', '.join(strPoint)}], Value: {self.funValue}"
        return repr_str

    def getSearchParameters(self):
        curr_var = self._variables[self._positionIndex]
        bound = []
        for step in (-self.oneStepSize, self.oneStepSize):
            bound.append(sorted([self.currentPos[self._positionIndex], self.currentPos[self._positionIndex] + step]))
        const_values = [(var, value) for var, value in zip(self._variables, self.currentPos) if var != curr_var]
        return bound, const_values

    def getFunctionValue(self, replace_val=None):
        eval_dict = dict(zip(self._variables, self.currentPos))
        if replace_val:
            eval_dict.update(replace_val)
        return self.fun.evaluate(eval_dict)

    def searchNextMove(self):
        bounds, const_val = self.getSearchParameters()
        nextMove = None
        newFunVal = None

        for bound in bounds:
            mini = goldenSectionSearch(self.fun, bound[0], bound[1], tuple(const_val), self.epsilon)
            miniVal = self.getFunctionValue({self._variables[self._positionIndex]: mini})
            if not newFunVal or newFunVal > miniVal:
                nextMove = mini
                newFunVal = miniVal
        return nextMove, newFunVal

    def switch

    def getLowestPos(self):
        iteration = 0
        while True:
            self.path.append(tuple(self.currentPos))
            localMinPosition, nextFunVal = self.searchNextMove()

            stepsLimitReached = iteration == self.stepsLimit
            minFunDifferenceReached = abs(self.funValue - nextFunVal) <= self.epsilon
            minPosDifferenceReached = np.linalg.norm(self.currentPos[self._positionIndex] - localMinPosition) <= self.epsilon

            if stepsLimitReached or (minPosDifferenceReached and minFunDifferenceReached):
                self.fun_minimum = tuple(self.currentPos)
                return tuple(self.currentPos)

            self.currentPos[self._positionIndex] = localMinPosition
            self.funValue = nextFunVal
            self._stepNumber += 1
            if self._positionIndex == len(self._variables) - 1:
                self._positionIndex = 0
            else:
                self._positionIndex += 1
            iteration += 1


if __name__ == '__main__':
    parser = Parser()
    ziaja_functions = [
        "x1^4+x2^4-0.62*x1^2-0.62*x2^2", 
        "2*x1^2-1.05*x1^4+1/6*x1^6+x1*x2+x2^2",  
        "x1^2-2.1*x1^4+1/3*x1^6+x1*x2-4*x2^2+4*x2^4", 
        "(x1^2+x2-11)^2+(x1+x2^2-7)^2-200",
        "x1^2+x1*x2+0.5*x2^2-x1-x2",
        "100*(x2-x1^2)^2+(1-x1)^2",
        "(x1-x2+x3)^2+(-x1+x2+x3)^2+(x1+x2-x3)^2",
        "x1*exp(-(x1^2+x2^2))",
        "x1^2+x2^2+x3^2-x1*x2+x1+2*x3",
        "(1+(x1+x2+1)^2*(19-14*x1+3*x1^2-14*x2+6*x1*x2+3*x2^2))"
        "*(30+(2*x1-3*x2)^2*(18-32*x1+12*x1^2+48*x2-36*x1*x2+27*x2^2))",
        "x1**2+x2**2"
    ]
    functions = [
        "x1**2+x2**2"
    ]

    x0 = [-10, -6]
    function = functions[0]
    print("function", function)
    function = parser.parse(function)

    cg = GaussSeidel(function, x0)
    pos = cg.getLowestPos()
    print("final pos: ", [round(x, 3) for x in pos])
    plot_path_graph(cg, graph_3d=False)
