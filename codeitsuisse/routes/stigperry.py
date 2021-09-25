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
    from_list = []
    to_list = []
    total_range = 0
    for q in questions:
        # Traverse through each question's set of ranges
        for i in q:
            to_list.append(i["to"])
            from_list.append(i["from"])
    mergeSort(from_list)
    mergeSort(to_list)
    total_range = to_list[-1] - from_list[0] + 1
    print(total_range)
    probability = Fraction(total_range,MAX)
    p = probability.numerator
    q = probability.denominator
    output = {}
    output["p"], output["q"] = p,q
    print(output)
    return output        

def mergeSort(arr):
    if len(arr) > 1:
  
         # Finding the mid of the array
        mid = len(arr)//2
        # Dividing the array elements
        L = arr[:mid]
  
        # into 2 halves
        R = arr[mid:]
  
        # Sorting the first half
        mergeSort(L)
  
        # Sorting the second half
        mergeSort(R)
  
        i = j = k = 0
  
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
  
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

for i in sample_input:
    processInterview(i)