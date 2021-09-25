import logging
import json
import requests

from flask import request, jsonify

from codeitsuisse import app

sample_input = [
    {
 "energy":2,
 "capital":500,
 "timeline":{
   "2037":{
     "Apple":{
       "price":100,
       "qty":10
     }
   },
   "2036":{
     "Apple":{
       "price":10,
       "qty":50
      }
   }
 }
}
]


logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def timeTravel():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for case in data:
        result.append(genOutput(case))
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def genOutput(case):
    return 1