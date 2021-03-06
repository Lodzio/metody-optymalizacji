import numpy as np
from py_expression_eval import Parser
from goldenSection import goldenSectionSearch
from plot import plot
from pyexcel_ods import save_data
from collections import OrderedDict

class GaussSeidel:
    def __init__(self, fun, g,startPoint, stepSize, epsilon, stepsLimit):
        self.fun = fun
        self.g = g
        self.epsilon = epsilon
        self.stepsLimit = stepsLimit
        self.stepSize = stepSize
        self.path = []
        self.stepNumber = 0
        self.sigma=[1, 1, 1, 1, 1]
        self.theta=[0, 0, 0, 0, 0]
        self.currentPos = np.array(startPoint, dtype="float")
        self.variables = sorted(fun.variables())
        self.funResult = self.getFunctionResult()
        self.e= np.array(np.eye(len(self.variables)))
        self.logs = []
        self.finalMatrix = [['x1', 'x2', 'f', 'c', 'iteracja']]

        self.vectors = []
        self.cmin = 0.1
        self.c0 = 1
        self.c = 1
        self.m1 = 0.25
        self.m2 = 10.0
        self.lastStep6 = False

    def __str__(self):
        parameters = dict(zip(self.variables, self.currentPos))
        strPoint = [str(round(axis, 2)) for axis in self.currentPos]
        strFVal = self.fun.evaluate(parameters)
        g = [f"g[{i+1}]={self.g[i].evaluate(parameters)}" for i in range(len(self.g))]
#         g1 = str(self.g[0].evaluate(parameters))
#         g2 = str(self.g[1].evaluate(parameters))
        c = str(self.getC(parameters))
        result = f"{self.stepNumber}: f({', '.join(strPoint)}) = {strFVal}, c: {c}, " + ','.join(g)
        transform = lambda value: str(round(value, 3))
        self.finalMatrix.append([transform(self.currentPos[0]), transform(self.currentPos[1]), transform(strFVal), transform(self.c), self.stepNumber])
        return result

    def calculatePunishment(self, parameters):
        sum = 0
        H = lambda x: 0 if x < 0 else 1
        for i in range(len(self.g)):
            gi = self.g[i]
            gVal= gi.evaluate(parameters)
            gArg = gVal + self.theta[i]
            deltaFun = self.sigma[i]*(gArg**2)*H(gArg)
            # print(gVal, H(gVal), deltaFun)
            sum+=deltaFun

        return sum

    def getFunctionResult(self, replace_val=None):
        parameters = dict(zip(self.variables, self.currentPos))
        if replace_val:
            parameters.update(replace_val)
        return self.fun.evaluate(parameters) + self.calculatePunishment(parameters)

    def getNextPosAndResult(self, pos, e):
        left = pos + e* (-self.stepSize)
        right = pos + e * (self.stepSize)
        left2 = pos + e* (-self.stepSize/4)
        right2 = pos + e * (self.stepSize/4)
        mini = goldenSectionSearch(self.variables, self.getFunctionResult, left, right, self.epsilon)
        miniVal = self.getFunctionResult(dict(zip(self.variables, mini)))
        return mini, miniVal

    def getNewE(self):
        nextPos = self.currentPos
        for i in range(len(self.e)):
            nextPos, nextFunResult = self.getNextPosAndResult(nextPos, self.e[i])
        diff = nextPos - self.currentPos
        # self.vectors.append([self.currentPos, pos1])
        # self.vectors.append([pos1, pos2])
        newE = diff/(np.linalg.norm(nextPos - self.currentPos))
        return self.e[0].copy()

    def getC(self, X):
        c = 0
        for i in range(len(self.g)):
            gi = self.g[i]
            gVal= gi.evaluate(X)
            if gVal + self.theta[i] > 0 and c < abs(gVal):
                c = abs(gVal)
        return c

    def switchMoveDirection(self, newE):
        for i in range(len(self.e)-1):
            self.e[i] = self.e[i+1]
        self.e[len(self.e)-1] = newE

    def step6(self, parameters):
        for i in range(len(self.g)):
            gVal = self.g[i].evaluate(parameters)
            if (self.c0*self.m1 > abs(gVal)) and (gVal + self.theta[i] > 0):
                self.theta[i]=self.theta[i]/self.m2
                self.sigma[i]=self.m2*self.sigma[i]
        self.lastStep6 = True

    def step8i(self, parameters):
        self.lastStep6 = False
        for i in range(len(self.g)):
            gVal = self.g[i].evaluate(parameters)
            self.theta[i] = max(gVal+self.theta[i], 0)

    def getLowestPos(self):
        while True:
            self.logs.append(str(self))
#             print(self)
            self.path.append(tuple(self.currentPos))
            localMinPosition, nextFunResult = self.getNextPosAndResult(self.currentPos, self.e[len(self.e)-1])
            self.c0 = self.c
            parameters = dict(zip(self.variables, localMinPosition))
            self.c = self.getC(parameters)
            stepsLimitReached = self.stepNumber == self.stepsLimit
            minFunDifferenceReached = abs(self.funResult - nextFunResult) <= self.epsilon
            minPosDifferenceReached = np.linalg.norm(self.currentPos- localMinPosition) <= self.epsilon
            cMinReached = self.cmin > self.c
            if stepsLimitReached or (minPosDifferenceReached and minFunDifferenceReached):
                return tuple(self.currentPos)
            if not cMinReached:
                if self.c < self.c0:
                    if self.stepNumber == 0 or self.lastStep6 == True:
                        self.step8i(parameters)
                    elif self.c<self.m1*self.c0:
                        self.step6(parameters)
                    else:
                        self.step8i(parameters)
                else:
                    self.c = self.c0
                    self.step6(parameters)
            self.currentPos = localMinPosition
            self.funResult = nextFunResult
            self.stepNumber += 1
            self.switchMoveDirection(self.getNewE())

if __name__ == '__main__':
    parser = Parser()
    functionStr = "(x1-2)^2+(x1-x2^2)^2"
    g=["x1+x2-2", "2*x1^2-x2"]
    x0 = [-10, 1.3]
    function = parser.parse(functionStr)
    cg = GaussSeidel(function, [parser.parse(gi) for gi in g], x0, 100, 10e-5, 3000)
    pos = cg.getLowestPos()

    print("final pos: ", [round(x, 3) for x in pos], 'f(x):', function.evaluate(dict(zip(sorted(function.variables()), pos))))
    print("g(x): ", [parser.parse(gi).evaluate(dict(zip(sorted(function.variables()), pos))) for gi in g])
#     if len(function.variables()) < 3:
#         plot(cg)

    # to gowno powinno byc wyodrebnione ale mi sie nie chce
    data = OrderedDict()
    data.update({"Sheet 1": cg.finalMatrix})
    save_data("result.ods", data)