import logging
import json

from flask import request, jsonify
from datetime import datetime

from codeitsuisse import app


def to_cumulative_delayed(stream: list, quantity_block: int):
    '''
    Assumptions:
    1. There could be multiple same ticks in the same timestamp but which set of tick that is added to the block does not have a particular order in this case

    '''
    if len(stream) == 0:
        return []
    # Process data
    split_list = []

    # Split each record within the list into timestamp, ticket, quantity, notional
    for record in stream:
        temp_array = record.split(',')
        # timestamp = datetime.strptime(temp_array[0], '%H:%M').strftime('%H:%M')
        timestamp = temp_array[0]
        ticker = temp_array[1]
        quantity = int(temp_array[2])
        price = float(temp_array[3])
        split_list.append([timestamp, ticker, quantity, price])

    # Sort by tickers first
    sorted_tickers_list = sorted(split_list, key=lambda x: x[1])

    # Group by tickers then sort by timestamp
    processed_list = []  # sorted by timestamp
    temp_array = [sorted_tickers_list[0]]

    for record in sorted_tickers_list[1:]:
        # Case 1 - If same ticker, append
        if record[1] == temp_array[-1][1]:
            temp_array.append(record)

        # Case 2 - Else, sort temp array and set it to new ticker
        else:
            processed_list += sorted(temp_array, key=lambda x: x[0])
            temp_array = [record]

    # Add in the last ticker temp array to processed list
    processed_list += sorted(temp_array, key=lambda x: x[0])

    # Cumulative Quantities in Blocks of Quantity Blocks

    print("processed_list")
    print(processed_list)
    # required_quantity works as a tracker
    required_quantity = quantity_block
    blocks_list = []
    current_timestamp = ""
    current_ticker = processed_list[0][1]
    current_quantity = 0
    current_notional = 0
    running = {}

    while len(processed_list) > 0:

        current_data = processed_list[0]

        # Case 1: If required_quantity is 0, add block into blocks_list
        if required_quantity == 0:
            # blocks_list.append(
            #     [current_timestamp, current_ticker, current_quantity, round(current_notional, 1)])

            if current_ticker not in running:
                running[current_ticker] = {"quantity": current_quantity, "notional": current_notional}
            else:
                running[current_ticker]["quantity"] = running[current_ticker]["quantity"] + current_quantity
                running[current_ticker]["notional"] = running[current_ticker]["notional"] + current_notional


            blocks_list.append([
                current_timestamp, current_ticker,
                str(running[current_ticker]["quantity"]),
                str(round(running[current_ticker]["notional"], 1))
            ])
            
            required_quantity = quantity_block
            current_quantity = 0
            current_notional = 0

        # Case 2: If required_quantity is more than 0 (meaning we still need to add to the block to reach desired quantity_block)
        elif required_quantity > 0:

            if current_data[1] == current_ticker:

                if current_data[2] == required_quantity:
                    current_timestamp = current_data[0]
                    current_quantity += current_data[2]
                    current_notional += (current_data[2] * current_data[3])
                    # Update required_quantity
                    required_quantity -= current_data[2]

                    # Remove from processed_list
                    processed_list.pop(0)
                elif current_data[2] < required_quantity:
                    if len(processed_list) == 1:
                        processed_list.pop(0)
                    elif current_ticker != processed_list[1][1]:
                        processed_list.pop(0)
                    else:
                        current_timestamp = current_data[0]
                        current_quantity += current_data[2]
                        current_notional += (current_data[2] * current_data[3])
                        required_quantity -= current_data[2]

                        processed_list.pop(0)

                else:
                    current_timestamp = current_data[0]
                    current_quantity += required_quantity
                    current_notional += (required_quantity * current_data[3])
                    processed_list[0][2] -= required_quantity
                    required_quantity = 0
            # If ticker is not the same, update current_ticker
            else:
                current_ticker = current_data[1]

    if current_quantity == quantity_block:
        # blocks_list.append([current_timestamp, current_ticker,
        #                    current_quantity, round(current_notional, 1)])
        if current_ticker not in running:
            running[current_ticker] = {"quantity": current_quantity, "notional": current_notional}
        else:
            running[current_ticker]["quantity"] = running[current_ticker]["quantity"] + current_quantity
            running[current_ticker]["notional"] = running[current_ticker]["notional"] + current_notional


        blocks_list.append([
            current_timestamp, current_ticker,
            str(running[current_ticker]["quantity"]),
            str(round(running[current_ticker]["notional"], 1))
        ])

    # Aggregate Data into List of Strings
    # Sort by timestamp
    sorted_result_list = sorted(
        blocks_list,
        key=lambda x:
        (datetime.strptime(x[0], '%H:%M').strftime('%H:%M')))

    # Aggregate all the same timestamp, into the same string
    result_final = []

    for record in sorted_result_list:

        timestamp = record[0]
        ticker = record[1]
        cumulative_quantity = str(record[2])
        cumulative_notional = str(record[3])

        # Empty, append first record
        if result_final == []:
            result_final.append(timestamp + ',' + ticker + ',' +
                                cumulative_quantity + ',' + cumulative_notional)

        # if not, check the timestamp (first 5 index)
        else:
            if timestamp == result_final[-1][0:5]:
                result_final[-1] += ',' + ticker + ',' + cumulative_quantity + ',' + cumulative_notional

            else:
                result_final.append(
                    timestamp + ',' + ticker + ',' + cumulative_quantity + ',' + cumulative_notional)

    output = { "output": result_final}

    return output


logger = logging.getLogger(__name__)


@app.route('/tickerStreamPart2', methods=['POST'])
def tickerStreamPart2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantityBlock = data.get("quantityBlock")

    result = to_cumulative_delayed(stream, quantityBlock)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
