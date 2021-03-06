import logging
import json
import sys
import itertools
from itertools import chain, combinations

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
    logging.info("data sent for evaluation {}".format(rooms))
    result = []
    for r in range(len(rooms)):
        result.append(checkInfection(rooms[r]))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def checkInfection(r):
    output = {}
    output["room"] = r["room"]
    output["p1"], output["p2"] = checkPA(r)
    output["p3"], output["p4"] = checkPB(r), checkPX(r)
    print(output)
    return output

def checkPA(r):
    grid = r["grid"]
    intInd = r["interestedIndividuals"]
    p1 = {} # p1 result
    p2 = 0 # p2 result

    grid_after = [len(grid)*[0] for _ in range(len(grid))]
    rows = len(grid)
    cols = len(grid[0])

    # No infections at all
    if rows ==1:
        for i in intInd:
            p1[i] = -1
        p2 = -1
        return p1,p2
    # Locate infected individual
    infected = ''
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 3:
                infected = (r,c)
                break
    # Scan the interested individuals and store result in p1
    for i in intInd:
        index = i.split(",")
        r = int(index[0])
        c = int(index[1])
        if grid[r][c] ==0 or grid[r][c] == 2 or grid[r][c] == 3: # Vacant space/Vaccinated/Already infected
            p1[i] = -1
        else: # Healthy
             # Generate shortest path from infected to individual
            p1[i] = findShortestPathLength_A(grid, infected, (r,c))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] ==0 or grid[r][c] == 2 or grid[r][c] == 3: # Vacant space/Vaccinated/Already infected
                continue
            else:
                dist = findShortestPathLength_A(grid, infected, (r,c))
                if dist == -1:
                    p2 = -1
                    break
                else:
                    p2 = max(p2,dist)
    return p1, p2

def checkPB(r):
    grid = r["grid"]
    rows = len(grid)
    cols = len(grid[0])

    p3 = 0 # p3 result
    infected = ''
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 3:
                infected = (r,c)
                break
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] ==0 or grid[r][c] == 2 or grid[r][c] == 3: # Vacant space/Vaccinated/Already infected
                continue
            else:
                dist = findShortestPathLength_B(grid, infected, (r,c))
                if dist == -1:
                    p3 = -1
                    break
                else:
                    p3 = max(p3,dist)
    return p3

def checkPX(r):
    return -1
    grid = r["grid"]
    intInd = r["interestedIndividuals"]
    grid_after = [len(grid)*[0] for _ in range(len(grid))]
    rows = len(grid)
    cols = len(grid[0])
    
    p4 = sys.maxsize # p4 result
    minP4 = p4

    # No infections at all
    if rows ==1:
        p4 = 0
    else:
        # Locate infected individuals and vacant spaces
        infected = '' 
        vacant = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 3:
                    infected = (r,c)
                elif grid[r][c] ==0:
                    vacant.append((r,c))
        # Traverse the grid and inspect each individual
        impossible = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] ==0 or grid[r][c] == 2 or grid[r][c] == 3: # Vacant space/Vaccinated/Already infected
                    continue
                elif grid[r][c] == 1: # Healthy
                    # Generate shortest path from infected to individual
                    grid_after[r][c] = findShortestPathLength_A(grid, infected, (r,c))
                    if grid_after[r][c] == -1:
                        impossible = True
        if impossible == False:
            return 0
            # Requires energy to remove vacant spaces
            # Loop through all vacant spaces one by one <BRUTE FORCE>
        else:
            for i in range(len(vacant)):
                for combo in itertools.combinations(vacant,1):
                    p4 = len(combo)
                    grid_new = grid
                    for i in combo:
                        grid_new[i[0]][i[1]] = 2
                    for r in range(rows):
                        for c in range(cols):
                            if grid_new[r][c] ==0 or grid_new[r][c] == 2 or grid_new[r][c] == 3: # Vacant space/Vaccinated/Already infected
                                continue
                            elif grid[r][c] == 1: # Healthy
                                # Generate shortest path from infected to individual
                                grid_after[r][c] = findShortestPathLength_A(grid_new, infected, (r,c))
                                if grid_after[r][c] == -1:
                                    continue 
                    return p4
    return p4
# Helper functions
def isSafe(mat, visited, x, y):
    return 0 <= x < len(mat) and 0 <= y < len(mat[0]) and \
           not (mat[x][y] == 0 or visited[x][y])
 
# Find the shortest possible route in a matrix `mat` from source cell (i, j)
# to destination cell `dest`.
 
# `min_dist` stores the length of the longest path from source to a destination
# found so far, and `dist` maintains the length of the path from a source cell to
# the current cell (i, j).
 
def findShortestPath_A(mat, visited, i, j, dest, min_dist=sys.maxsize, dist=0):
    # if the destination is found, update `min_dist`
    if (i, j) == dest:
        return min(dist, min_dist)
 
    # set (i, j) cell as visited
    visited[i][j] = 1
 
    # go to the bottom cell
    if isSafe(mat, visited, i + 1, j):
        min_dist = findShortestPath_A(mat, visited, i + 1, j, dest, min_dist, dist + 1)
 
    # go to the right cell
    if isSafe(mat, visited, i, j + 1):
        min_dist = findShortestPath_A(mat, visited, i, j + 1, dest, min_dist, dist + 1)
 
    # go to the top cell
    if isSafe(mat, visited, i - 1, j):
        min_dist = findShortestPath_A(mat, visited, i - 1, j, dest, min_dist, dist + 1)
 
    # go to the left cell
    if isSafe(mat, visited, i, j - 1):
        min_dist = findShortestPath_A(mat, visited, i, j - 1, dest, min_dist, dist + 1)
 
    # backtrack: remove (i, j) from the visited matrix
    visited[i][j] = 0
 
    return min_dist
 
# Wrapper over findShortestPath_A() function
def findShortestPathLength_A(mat, src, dest):
    # get source cell (i, j)
    i, j = src
 
    # get destination cell (x, y)
    x, y = dest
 
    # base case
    if not mat or len(mat) == 0 or mat[i][j] == 0 or mat[x][y] == 0:
        return -1
 
    # `M ?? N` matrix
    (M, N) = (len(mat), len(mat[0]))
 
    # construct an `M ?? N` matrix to keep track of visited cells
    visited = [[False for _ in range(N)] for _ in range(M)]
 
    min_dist = findShortestPath_A(mat, visited, i, j, dest)
 
    if min_dist != sys.maxsize:
        return min_dist
    else:
        return -1

def findShortestPath_B(mat, visited, i, j, dest, min_dist=sys.maxsize, dist=0):
    # if the destination is found, update `min_dist`
    if (i, j) == dest:
        return min(dist, min_dist)
 
    # set (i, j) cell as visited
    visited[i][j] = 1
 
    # go to the bottom cell
    if isSafe(mat, visited, i + 1, j):
        min_dist = findShortestPath_B(mat, visited, i + 1, j, dest, min_dist, dist + 1)
 
    # go to the right cell
    if isSafe(mat, visited, i, j + 1):
        min_dist = findShortestPath_B(mat, visited, i, j + 1, dest, min_dist, dist + 1)
 
    # go to the top cell
    if isSafe(mat, visited, i - 1, j):
        min_dist = findShortestPath_B(mat, visited, i - 1, j, dest, min_dist, dist + 1)
 
    # go to the left cell
    if isSafe(mat, visited, i, j - 1):
        min_dist = findShortestPath_B(mat, visited, i, j - 1, dest, min_dist, dist + 1)
    
    # go to the diagonal cells
    # Bottom right
    if isSafe(mat, visited, i + 1, j + 1):
        min_dist = findShortestPath_B(mat, visited, i + 1, j + 1, dest, min_dist, dist + 1)
    # Bottom left
    if isSafe(mat, visited, i + 1, j - 1):
        min_dist = findShortestPath_B(mat, visited, i + 1, j - 1, dest, min_dist, dist + 1)
    # Top right
    if isSafe(mat, visited, i - 1, j + 1):
        min_dist = findShortestPath_B(mat, visited, i - 1, j + 1, dest, min_dist, dist + 1)
    # Top left
    if isSafe(mat, visited, i - 1, j - 1):
        min_dist = findShortestPath_B(mat, visited, i - 1, j - 1, dest, min_dist, dist + 1)
 
    # backtrack: remove (i, j) from the visited matrix
    visited[i][j] = 0
 
    return min_dist
 
# Wrapper over findShortestPath_B() function
def findShortestPathLength_B(mat, src, dest):
    # get source cell (i, j)
    i, j = src
 
    # get destination cell (x, y)
    x, y = dest
 
    # base case
    if not mat or len(mat) == 0 or mat[i][j] == 0 or mat[x][y] == 0:
        return -1
 
    # `M ?? N` matrix
    (M, N) = (len(mat), len(mat[0]))
 
    # construct an `M ?? N` matrix to keep track of visited cells
    visited = [[False for _ in range(N)] for _ in range(M)]
 
    min_dist = findShortestPath_B(mat, visited, i, j, dest)
 
    if min_dist != sys.maxsize:
        return min_dist
    else:
        return -1

def powerset(iterable):
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

for i in sample_input:
    checkInfection(i)