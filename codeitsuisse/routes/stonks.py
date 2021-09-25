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
   },
   "2033":{
  "Apple":{
    "price": 90,
    "qty":10
   }
},
"2034":{
  "Apple":{
    "price": 70,
    "qty":5
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
    return json.dumps(result, indent = 4)

def genOutput(case):
    energy = case["energy"]
    capital = case["capital"]
    timeline = case["timeline"]
    years = []
    for key in timeline:
      years.append((key,timeline[key]["Apple"]["price"]))
    # Sort the years according to the lowest prices
    print("UNSORTED:", years)
    mergeSort(years)
    print("SORTED: ", years)
    
    # Maximise the total quantity of stocks that can be purchased less than price in 2037
    queue = []
    total_visited = 0
    total_cost = 0
    
    # if years[0][0] != '2037':
      # queue.append(('Jump', 2037, years[0][0])) # First jump
      # energy-=1
      # queue.append('')

    # while energy>2:
      # price = years[start][1]
      # quantity = timeline[years[start][0]]["qty"]
      # total_cost += price*quantity
      # if total_cost < capital:
        # queue.append("j-")
      # else:
        # total_cost -= price*quantity
        # corrected_qty =  (capital - total_cost)//price
        # queue.append("")
      # start+=1
# 
    # Jump to highest price before going back to 2037
    # if years[-1][0] != '2037':

    # else: # Jump to year 
      # 

    
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
            if L[i][1] < R[j][1]:
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
  genOutput(i)