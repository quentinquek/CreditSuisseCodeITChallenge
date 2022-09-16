import logging
import json

from flask import request, jsonify
from datetime import datetime

from codeitsuisse import app

def to_cumulative(stream: list):
    """
  Assumptions:
  1. There could be multiple same ticks in the same timestamp with different price and quantity (E.g. There could be 2 ticks of "A" at "00:00" with different price and quantity)
  2. For cumulative_quantity and cumulative_notional, it is computed cumulatively for that certain timestap. (E.g. With data ['00:00,A,1,2.0', '00:00,A,3,5.0', '00:11,A,3,4.0'], will give the result of ['00:00,A,4,17.0','00:11,A,3,12.0'])
  """
  
    result_list = []

    # Split each record within the list into timestamp, ticket, quantity, notional
    for record in stream:
        temp_array = record.split(',')
        # timestamp = datetime.strptime(temp_array[0], '%H:%M').strftime('%H:%M')
        timestamp = temp_array[0]
        ticker = temp_array[1]
        quantity = int(temp_array[2])
        price = float(temp_array[3])

        result_list.append([timestamp, ticker, quantity, price])

    # Sort by timestamp and tickers
    sorted_result_list = sorted(
        result_list,
        key=lambda x:
        (datetime.strptime(x[0], '%H:%M').strftime('%H:%M'), x[1]))

    prev_timestamp = sorted_result_list[0][0]
    prev_ticker = sorted_result_list[0][1]
    prev_cumulative_quantity = 0
    prev_cumulative_notional = 0

    result_list_unaggregated = []

    # Merge by same timestamp and tickers, get cumulative_quantiy and cumulative_notional
    for record in sorted_result_list:

        # Case 1 - Same timestamp
        if datetime.strptime(prev_timestamp,
                             '%H:%M') == datetime.strptime(record[0], '%H:%M'):

            # Case 1.1 - same ticker, add quantiy and notional to previous
            if (prev_ticker == record[1]):

                prev_cumulative_quantity += record[2]
                prev_cumulative_notional += record[2] * record[3]

            # Case 1.2 - different ticker, append previous to result array
            else:
                result_list_unaggregated.append([
                    prev_timestamp, prev_ticker,
                    str(prev_cumulative_quantity),
                    str(prev_cumulative_notional)
                ])

                # set previous to current
                prev_timestamp = record[0]
                prev_ticker = record[1]
                prev_cumulative_quantity = record[2]
                prev_cumulative_notional = record[2] * record[3]

        # Case 2 - Different timestamp
        else:
            result_list_unaggregated.append([
                prev_timestamp, prev_ticker,
                str(prev_cumulative_quantity),
                str(prev_cumulative_notional)
            ])

            # set previous to current
            prev_timestamp = record[0]
            prev_ticker = record[1]
            prev_cumulative_quantity = record[2]
            prev_cumulative_notional = record[2] * record[3]

    # End of for loop, append the last one
    result_list_unaggregated.append([
        prev_timestamp, prev_ticker,
        str(prev_cumulative_quantity),
        str(prev_cumulative_notional)
    ])

    # Aggregate all the same timestamp, into the same string
    result_final = []

    for record in result_list_unaggregated:

        # Empty, append first record
        if result_final == []:
            result_final.append(','.join(record))

        # if not check the timestamp (first 5 index)
        else:
            if record[0] == result_final[-1][0:5]:
                record.pop(0)
                result_final[-1] += ',' + ','.join(record)

            else:
                result_final.append(','.join(record))

    output = { "output": result_final}

    return output

    # raise Exception

logger = logging.getLogger(__name__)


@app.route('/tickerStreamPart1', methods=['POST'])
def tickerStreamPart1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    # print("Testing code...")
    result = to_cumulative(inputValue)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

