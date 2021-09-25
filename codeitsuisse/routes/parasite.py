import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")

    result = []
    for test_case in data:
        result.append(checkInfection(test_case["room"],test_case["grid"], test_case["interestedIndividuals"]))
    logging.info("My result :{}".format(result))
    return jsonify(result)

def checkInfection(room,grid,interestedIndividuals):
    result["room"] = room
    result["p1"]= checkP1(room,grid,interestedIndividuals)
    result["p2"] = 0
    result["p3"] = 0
    return result 

def checkP1(room,grid,interestIndividuals):
    for i in interestedIndividuals:
        print("INterestedIndidivuals: ", i)
    output = {}
    output["HELLO"] = "world"
    return output

def checkP2(room,grid):
    return nil

def checkP3(room,grid):
    return nil

def checkP4(room,grid):
    return nil

