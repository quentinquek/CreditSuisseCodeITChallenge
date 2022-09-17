import logging
import json

from flask import request, jsonify

from codeitsuisse import app


@app.route('/reversle', methods=['POST'])
def reversle():
    data = request.get_json()
    logging.info("data sent for evaluation ")

    # logging.info("data size: " + str(len(data)))
    # logging.info("data sent for evaluation {}".format(data))
    answers = data.get("answers")
    attempts = data.get("attempts")
    numbers = data.get("numbers")
    result_1 = quordle_part_1(answers, attempts)
    numGrey = result_1[0]
    leftovers = result_1[1]
    result_2 = quordle_part_2(numGrey, leftovers, numbers)

    result = {
        "part1": numGrey,
        "part2": result_2
    }

    # result = max_lifetime(json.loads(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)