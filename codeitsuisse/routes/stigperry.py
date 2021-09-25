import logging
import json
from fractions import Fraction

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
sample_input = [
    {
        "questions": [
            [{
                "from": 2,
                "to": 4
            },
            {
                "from": 3,
                "to": 5
            }
            ]
        ] ,
        "coefficients": [
            {
                "p": 0,
                "q": 0
            },
            {
                "p": 0,
                "q": 0
            }
        ],
        "maxRating": 1000000000
    }
]


@app.route('/stig/perry', methods=['POST'])
def evaluateInterviews():
    interviews = request.get_json()
    logging.info("interviews sent for evaluation {}".format(interviews))
    result = []
    for i in interviews:
        result.append(processInterview(i))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def processInterview(i):
    questions = i["questions"]
    MAX = i["maxRating"]
    min_val = questions[0][0]["from"]
    max_val = questions[0][0]["to"]
    total_range = 0
    for q in questions:
        # Traverse through each question's set of ranges
        for i in q:
            min_val = min(i["from"], min_val)
            max_val = max(i["to"], max_val)
    total_range = max_val - min_val + 1
    probability = Fraction(total_range,MAX)
    p = probability.numerator
    q = probability.denominator
    output = {}
    output["p"], output["q"] = p,q
    return output        
# for i in sample_input:
    # processInterview(i)



