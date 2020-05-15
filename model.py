import numpy as np
from py_expression_eval import Parser
from goldenSection import goldenSectionSearch
from graphs import plot


class GaussSeidel:
    def __init__(self, fun, startPoint, oneStepSize, epsilon, stepsLimit):
        self.fun = fun
        self.epsilon = epsilon
        self.stepsLimit = stepsLimit
        self.oneStepSize = oneStepSize
        self.path = []
        self.positionIndex = 0
        self.stepNumber = 0
        self.currentPos = np.array(startPoint, dtype="float")
        self.variables = sorted(fun.variables())
        self.funResult = self.getFunctionResult()

    def __str__(self):
        strPoint = [str(round(axis, 3)) for axis in self.currentPos]
        result = f"{self.stepNumber}: f({', '.join(strPoint)}) = {self.funResult}"
        return result

    def getFunctionResult(self, replace_val=None):
        parameters = dict(zip(self.variables, self.currentPos))
        if replace_val:
            parameters.update(replace_val)
        return self.fun.evaluate(parameters)
    
    def getSearchBoundsAndVar(self):
        curr_var = self.variables[self.positionIndex]
        bound = []
        for step in (-self.oneStepSize, self.oneStepSize):
            bound.append(sorted([self.currentPos[self.positionIndex], self.currentPos[self.positionIndex] + step]))
        variable = [(var, value) for var, value in zip(self.variables, self.currentPos) if var != curr_var]
        return bound, variable

    def getNextPosAndResult(self):
        bounds, variable = self.getSearchBoundsAndVar()
        nextPos = None
        newFunResult = None

        for bound in bounds:
            mini = goldenSectionSearch(self.fun, bound[0], bound[1], tuple(variable), self.epsilon)
            miniVal = self.getFunctionResult({self.variables[self.positionIndex]: mini})
            if not newFunResult or newFunResult > miniVal:
                nextMove = mini
                newFunResult = miniVal
        return nextMove, newFunResult

    def switchMoveDirection(self):
        if self.positionIndex == len(self.variables) - 1:
            self.positionIndex = 0
        else:
            self.positionIndex += 1

    def getLowestPos(self):
        while True:
            print(self)
            self.path.append(tuple(self.currentPos))
            localMinPosition, nextFunResult = self.getNextPosAndResult()

            stepsLimitReached = self.stepNumber == self.stepsLimit
            minFunDifferenceReached = abs(self.funResult - nextFunResult) <= self.epsilon
            minPosDifferenceReached = np.linalg.norm(self.currentPos[self.positionIndex] - localMinPosition) <= self.epsilon

            if stepsLimitReached or (minPosDifferenceReached and minFunDifferenceReached):
                return tuple(self.currentPos)

            self.currentPos[self.positionIndex] = localMinPosition
            self.funResult = nextFunResult
            self.stepNumber += 1
            self.switchMoveDirection()


if __name__ == '__main__':
    parser = Parser()
    functions = [
        "x1^2+x2^2+(x1*x2)^2",
    ]

    x0 = [-10, -6]
    function = functions[0]
    print("function", function)
    function = parser.parse(function)

    cg = GaussSeidel(function, x0, 2, 10e-3, 3000)
    pos = cg.getLowestPos()
    print("final pos: ", [round(x, 3) for x in pos])
    plot(cg)
