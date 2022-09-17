import logging
import json

from flask import request, jsonify
from datetime import datetime

from codeitsuisse import app

def max_lifetime(data_input):
    print(data_input)

    max_lifetime_history = {}
    # seen_values = []
    result = []

    for each_input in data_input:
        corresponding_max = []
        for each_val in each_input:
            print("different val")
            print(each_val)
            all_values = []

            '''
            Idea:
            1. If not in all_values, I will keep going
            2. Stop if I see curr_val in all_values
            3. At every curr_val I will store and update max of it in max_lifetime_history
            '''
            if each_val not in max_lifetime_history:
                # Calculate max lifetime
                max = each_val
                all_values.append(each_val)
                max_lifetime_history[each_val] = max
                
                curr_val = each_val

                # If value is even
                if curr_val % 2 == 0:
                    curr_val = curr_val // 2
                # If value is odd 
                else:
                    curr_val = curr_val * 3 + 1

                print(all_values)
                print("curr_val" + str(curr_val))
                
                while curr_val not in all_values:
                    print(curr_val)
                    all_values.append(curr_val)

            

                    if curr_val > max:
                        max = curr_val
                        # max_lifetime_history[curr_val] = max

                        for num in all_values:
                            max_lifetime_history[num] = max
                    
                    if curr_val % 2 == 0:
                        curr_val = curr_val // 2
                    # If value is odd 
                    else:
                        curr_val = curr_val * 3 + 1
                


                # while curr_val > max:
                #     max = curr_val

                #     if curr_val % 2 == 0:
                #         curr_val /= 2
                #     # If value is odd 
                #     else:
                #         curr_val = curr_val * 3 + 1


                
                max_lifetime_history[each_val] = max
                corresponding_max.append(max)
            
            else:
                corresponding_max.append(max_lifetime_history[each_val])

        result.append(corresponding_max)
    
    return result



@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # stream = data.get("stream")
    result = max_lifetime(data)

    # result = max_lifetime(json.loads(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)