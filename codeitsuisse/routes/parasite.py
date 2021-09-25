import logging
import json
import sys

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

sample_input = [
  {
    "room": 1,
    "grid": [
      [0, 3],
      [0, 1]
    ],
    "interestedIndividuals": [
      "0,0"
    ]
  },
  {
    "room": 2,
    "grid": [
      [0, 3, 2],
      [0, 1, 1],
      [1, 0, 0]
    ],
    "interestedIndividuals": [
      "0,2", "2,0", "1,2"
    ]
  }
]
@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    rooms = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for r in rooms:
        result.append(checkInfection(r))
    logging.info("My result :{}".format(result))
    return jsonify(result)

def checkInfection(r):
    output = {}
    output["room"] = r["room"]
    output["p1"] = checkP1(r)
    output["p2"] = checkP2(r)
    output["p3"] = checkP3(r)
    output["p4"] = checkP4(r)
    return output

def checkP1(r):
    grid = r["grid"]
    intInd = r["interestedIndividuals"]
    grid_after = [len(grid)*[0] for _ in range(len(grid))]
    p1 = {}
    rows = len(grid)
    cols = len(grid[0])
    # No infections at all
    if not checkInfected(grid) or rows ==1:
        for i in intInd:
            p1[i] = -1
    else:
        # Locate infected individual
        infected = ''
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 3:
                    infected = (r,c)
        # Traverse the grid and inspect each individual
        safe = True
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] ==0 or grid[r][c] == 2 or grid[r][c] == 3: # Vacant space/Vaccinated/Already infected
                    grid_after[r][c]=-1
                elif grid[r][c] == 1: # Healthy
                    print("CHECKING HEALTHY")
                    # Check the individual's left/right/bottom/top
                    if (r-1)>=0:
                        if grid[r-1][c] !=0:
                            safe = False
                    if r+1<rows:
                        if grid[r+1][c]!=0:
                            safe = False
                    if c-1>=0:
                        if grid[r][c-1] !=0:
                            safe = False
                    if c+1<cols:
                        if grid[r][c+1]!=0:
                            safe = False
                    if safe:
                        grid[r][c]=-1 # Individual is safe
                        # continue
                    # Generate shortest path from infected to individual
                    grid_after[r][c] = findShortestPathLength(grid, infected, (r,c))
    # Scan the interested individuals and store result in p1
    for i in intInd:
        index = i.split(",")
        p1[i] = grid_after[int(index[0])][int(index[1])]
    return p1

def checkP2(r):
    return 99

def checkP3(r):
    return 99

def checkP4(r):
    return 99

# Helper functions

def checkInfected(grid):
    r = len(grid)
    c = len(grid[0])
    for i in range(r):
        for j in range(c):
            if grid[i][j] ==3:
                return True
    return False

def isSafe(mat, visited, x, y):
    return 0 <= x < len(mat) and 0 <= y < len(mat[0]) and \
           not (mat[x][y] == 0 or visited[x][y])
 
 
# Find the shortest possible route in a matrix `mat` from source cell (i, j)
# to destination cell `dest`.
 
# `min_dist` stores the length of the longest path from source to a destination
# found so far, and `dist` maintains the length of the path from a source cell to
# the current cell (i, j).
 
def findShortestPath(mat, visited, i, j, dest, min_dist=sys.maxsize, dist=0):
    # if the destination is found, update `min_dist`
    if (i, j) == dest:
        return min(dist, min_dist)
 
    # set (i, j) cell as visited
    visited[i][j] = 1
 
    # go to the bottom cell
    if isSafe(mat, visited, i + 1, j):
        min_dist = findShortestPath(mat, visited, i + 1, j, dest, min_dist, dist + 1)
 
    # go to the right cell
    if isSafe(mat, visited, i, j + 1):
        min_dist = findShortestPath(mat, visited, i, j + 1, dest, min_dist, dist + 1)
 
    # go to the top cell
    if isSafe(mat, visited, i - 1, j):
        min_dist = findShortestPath(mat, visited, i - 1, j, dest, min_dist, dist + 1)
 
    # go to the left cell
    if isSafe(mat, visited, i, j - 1):
        min_dist = findShortestPath(mat, visited, i, j - 1, dest, min_dist, dist + 1)
 
    # backtrack: remove (i, j) from the visited matrix
    visited[i][j] = 0
 
    return min_dist
 
 
# Wrapper over findShortestPath() function
def findShortestPathLength(mat, src, dest):
 
    # get source cell (i, j)
    i, j = src
 
    # get destination cell (x, y)
    x, y = dest
 
    # base case
    if not mat or len(mat) == 0 or mat[i][j] == 0 or mat[x][y] == 0:
        return -1
 
    # `M × N` matrix
    (M, N) = (len(mat), len(mat[0]))
 
    # construct an `M × N` matrix to keep track of visited cells
    visited = [[False for _ in range(N)] for _ in range(M)]
 
    min_dist = findShortestPath(mat, visited, i, j, dest)
 
    if min_dist != sys.maxsize:
        return min_dist
    else:
        return -1

print(checkInfection(sample_input[0]))