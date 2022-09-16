import logging
import json

from flask import request, jsonify
from datetime import datetime

from codeitsuisse import app

@app.route('/square', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

# @app.route('/tickerStreamPart1', methods=['POST'])
# def evaluate():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     inputValue = data.get("stream")
#     # print("Testing code...")
#     result = to_cumulative(inputValue)
#     logging.info("My result :{}".format(result))
#     return json.dumps(inputValue)

