import logging
import json
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST', 'GET'])
def playGame():
    if request.method == 'POST':
        data = request.get_json()
        logging.info("data sent for evaluation {}".format(data))
        result = data.get("battleId")
        logging.info("My result :{}".format(result))
        request.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/"+result)
        res = requests.post('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/', json=dictToSend)
        return json.dumps(result)
        

