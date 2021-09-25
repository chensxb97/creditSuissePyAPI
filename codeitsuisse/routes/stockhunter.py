import logging
import json
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
        result.append(processStocks(s))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def processStocks(s):
    return



for s in sample_input:
    processStocks(s)


