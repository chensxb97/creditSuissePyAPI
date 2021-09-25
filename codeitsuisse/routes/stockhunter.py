import logging
import json
import sys
from fractions import Fraction

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
sample_input = [{
    "entryPoint":{
        "first": 0,
        "second": 0
        },
    "targetPoint":{
        "first": 2,
        "second": 2
        },
    "gridDepth": 156,
    "gridKey":20183,
    "horizontalStepper":16807,
    "verticalStepper":48271
}]

@app.route('/stock-hunter', methods=['POST'])
def stockHunting():
    stocks = request.get_json()
    logging.info("interviews sent for evaluation {}".format(stocks))
    result = []
    for s in stocks:
        output = processStocks(s)
        result.append(output)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def processStocks(s):
    eP = s["entryPoint"]
    tP = s["targetPoint"]
    x, y = eP["first"], eP["second"]
    xT, yT = tP["first"],tP["second"]
    gridKey = s["gridKey"]
    gridDepth = s["gridDepth"]
    hStep = s["horizontalStepper"]
    vStep = s["verticalStepper"]

    rows = abs(yT-y)+1
    cols = abs(xT-x)+1
    gridMap = [[0]*(cols) for _ in range(rows)]
    value_gridMap =[[0]*(cols) for _ in range(rows)]
    # Compute the cost and assign gridMap
    computedValues = [[0]*(cols) for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            riskLevel = computeRiskLevel(x,y,hStep,vStep,gridKey,gridDepth,computedValues)
            # print("Risklevel for x y ", x,y,": ", riskLevel)
            if riskLevel%3 ==0:
                gridMap[y][x] = "L"
                value_gridMap[y][x] = 3
            elif riskLevel%3 ==1:
                gridMap[y][x] = "M"
                value_gridMap[y][x] = 2
            elif riskLevel%3 ==2:
                gridMap[y][x] = "S"
                value_gridMap[y][x] = 1

    # print(gridMap)
    output = {}
    output["gridMap"] = gridMap
    output["minimumCost"] = minCost(value_gridMap,xT,yT)
    return output

def computeRiskLevel(x,y,hStep,vStep,gridKey,gridDepth,computedValues):
    if computedValues[x][y] !=0:
        return computedValues[x][y]
    if x ==0 and y ==0:
        computedValues[x][y] = gridDepth%gridKey
    elif x ==0:
        computedValues[x][y] = (y*vStep+gridDepth)%gridKey
    elif y ==0:
        computedValues[x][y] = (x*hStep+gridDepth)%gridKey
    else:
        computedValues[x][y] = (computeRiskLevel(x-1,y,hStep,vStep,gridKey,gridDepth,computedValues)*computeRiskLevel(x,y-1,hStep,vStep,gridKey,gridDepth,computedValues)+gridDepth)%gridKey

    return computedValues[x][y]
# Returns cost of minimum cost path from (0,0) to (m, n) in mat[R][C]
def minCost(cost, m, n):
    if (n < 0 or m < 0):
        return sys.maxsize
    elif (m == 0 and n == 0):
        return cost[m][n]
    else:
        return cost[m][n] + min( minCost(cost, m-1, n-1),
                                minCost(cost, m-1, n),
                                minCost(cost, m, n-1) )
def min(x, y, z):
    if (x < y):
        return x if (x < z) else z
    else:
        return y if (y < z) else z
# for s in sample_input:
    # print(processStocks(s))


