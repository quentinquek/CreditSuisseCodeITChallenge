import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/square', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

@app.route("/tickerStreamPart1", methods=["POST"])
def evaluate_ticker_p1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    logging.info("My result :{}".format(inputValue))
    return json.dumps(inputValue)

