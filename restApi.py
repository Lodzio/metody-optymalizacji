from flask import Flask, request
from flask_cors import CORS, cross_origin
from model import GaussSeidel
from py_expression_eval import Parser
import json 
from plot import plot
from multiprocessing import Process
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cg = 0

def showGraph(function, g, startPoint, localStepSize, epsilon, stepsLimit):
    cg = GaussSeidel(function, g, startPoint, localStepSize, epsilon, stepsLimit)
    pos = cg.getLowestPos()
    plot(cg)


@app.route('/', methods=['GET'])
@cross_origin()
def calculate():
    g = []
    parser = Parser()
    function = request.args.get('function')
    g1 = request.args.get('g1')
    g2 = request.args.get('g2')
    g3 = request.args.get('g3')
    g4 = request.args.get('g4')
    g5 = request.args.get('g5')
    x3 = request.args.get('x3')
    x4 = request.args.get('x4')
    x5 = request.args.get('x5')

    g1 and g.append(g1)
    g2 and g.append(g2)
    g3 and g.append(g3)
    g4 and g.append(g4)
    g5 and g.append(g5)

    g = [parser.parse(gi) for gi in g]

    startPoint = [float(request.args.get('x1')), float(request.args.get('x2'))]
    x3 and startPoint.append(x3)
    x4 and startPoint.append(x4)
    x5 and startPoint.append(x5)
    print("new run", function, g1, g2, g3, startPoint)
    localStepSize = float(request.args.get('localStepSize', '50'))
    epsilon = float(request.args.get('epsilon', '10e-3'))
    stepsLimit = int(request.args.get('stepsLimit', '3000'))
    function = parser.parse(function)
    if len(function.variables()) < 3: 
        Process(target=showGraph, args=(function, g, startPoint, localStepSize, epsilon, stepsLimit)).start()
    cg = GaussSeidel(function, g, startPoint, localStepSize, epsilon, stepsLimit)
    pos = cg.getLowestPos()
    parameters = dict(zip(cg.variables, pos))
    result = {
        "pos": pos,
        "logs": cg.logs,
        "f": function.evaluate(parameters),
        "g": [gi.evaluate(dict(zip(sorted(function.variables()), pos))) for gi in g]
    }
    return result



if __name__ == '__main__':
    app.run(debug=True)