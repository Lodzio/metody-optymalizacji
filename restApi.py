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
    g1 and g.append(g1)
    g2 and g.append(g2)
    g3 and g.append(g3)
    g = [parser.parse(gi) for gi in g]

    startPoint = [float(request.args.get('x1')), float(request.args.get('x2'))]
    print(function, g1, g2, g3, startPoint)
    localStepSize = float(request.args.get('localStepSize', 10))
    epsilon = float(request.args.get('epsilon', 10e-3))
    stepsLimit = int(request.args.get('stepsLimit', 3000))
    function = parser.parse(function)
    Process(target=showGraph, args=(function, g, startPoint, localStepSize, epsilon, stepsLimit)).start()
    cg = GaussSeidel(function, g, startPoint, localStepSize, epsilon, stepsLimit)
    pos = cg.getLowestPos()
    result = {
        "pos": pos,
        "logs": cg.logs,
        "g": [gi.evaluate({"x1": pos[0], "x2": pos[1]}) for gi in g]
    }
    return result



if __name__ == '__main__':
    app.run(debug=True)