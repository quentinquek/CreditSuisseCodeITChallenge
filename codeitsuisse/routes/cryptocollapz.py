import logging
import json

from flask import request, jsonify
from datetime import datetime

from codeitsuisse import app

# def max_lifetime(data_input):
#     # print(data_input)
#     # print(len(data_input))

#     max_lifetime_history = {}
#     # seen_values = []
#     result = []

#     for each_input in data_input:
#         corresponding_max = []
#         for each_val in each_input:
#             # print("different val")
#             # print(each_val)
#             all_values = []

#             '''
#             Idea:
#             1. If not in all_values, I will keep going
#             2. Stop if I see curr_val in all_values
#             3. At every curr_val I will store and update max of it in max_lifetime_history
#             '''
#             if each_val not in max_lifetime_history:
#                 # Calculate max lifetime
#                 max = each_val
#                 all_values.append(each_val)
#                 max_lifetime_history[each_val] = max
                
#                 curr_val = each_val

#                 num_divide = 0

#                 # If value is even
#                 if curr_val % 2 == 0:
#                     curr_val = curr_val // 2
#                     num_divide += 1
#                 # If value is odd 
#                 else:
#                     curr_val = curr_val * 3 + 1
                    

#                 # print(all_values)
#                 # print("curr_val" + str(curr_val))
                
#                 # while curr_val not in all_values:
#                 #     # print(curr_val)
#                 #     all_values.append(curr_val)

#                 #     # if curr_val not in max_lifetime_history:
#                 #     #     max_lifetime_history[curr_val] = curr_val

#                 #     if curr_val > max:
#                 #         max = curr_val
#                 #         # max_lifetime_history[curr_val] = max

#                 #         for num in all_values:
#                 #             max_lifetime_history[num] = max
                    
#                 #     if curr_val % 2 == 0:
#                 #         curr_val = curr_val // 2
#                 #     # If value is odd 
#                 #     else:
#                 #         curr_val = curr_val * 3 + 1

#                 if each_val < 100:

#                     while curr_val not in all_values:
#                         print("curr_val: " + str(curr_val))
#                         all_values.append(curr_val)

#                         # if curr_val not in max_lifetime_history:
#                         #     max_lifetime_history[curr_val] = curr_val

#                         if curr_val > max:
#                             max = curr_val
#                             # max_lifetime_history[curr_val] = max

#                             for num in all_values:
#                                 max_lifetime_history[num] = max
                        
#                         if curr_val % 2 == 0:
#                             curr_val = curr_val // 2
#                         # If value is odd 
#                         else:
#                             curr_val = curr_val * 3 + 1

#                 # ======= Logic - if we divde 2 times, it is hard to recover to be bigger than max =======
#                 else:
#                     print("curr_val:" + str(curr_val))
                    
#                     while num_divide < 2:
#                         # print(curr_val)
#                         print("num_divide:" + str(num_divide))
#                         all_values.append(curr_val)

#                         # if curr_val not in max_lifetime_history:
#                         #     max_lifetime_history[curr_val] = curr_val

#                         if curr_val > max:
#                             max = curr_val
#                             # max_lifetime_history[curr_val] = max

#                             for num in all_values:
#                                 max_lifetime_history[num] = max
                        
#                         if curr_val % 2 == 0:
#                             curr_val = curr_val // 2
#                             num_divide += 1
#                         else:
#                             curr_val = curr_val * 3 + 1 
#                             num_divide = 0

#                 print("max:" + str(max))
#                 max_lifetime_history[each_val] = max
#                 corresponding_max.append(max)
            
#             else:
#                 corresponding_max.append(max_lifetime_history[each_val])

#         result.append(corresponding_max)

#     # for each_val in data_input:
#     #     print("different val")
#     #     print(each_val)
#     #     all_values = []

#     #     '''
#     #     Idea:
#     #     1. If not in all_values, I will keep going
#     #     2. Stop if I see curr_val in all_values
#     #     3. At every curr_val I will store and update max of it in max_lifetime_history
#     #     '''
#     #     if each_val not in max_lifetime_history:
#     #         # Calculate max lifetime
#     #         max = each_val
#     #         all_values.append(each_val)
#     #         max_lifetime_history[each_val] = max
            
#     #         curr_val = each_val

#     #         # If value is even
#     #         if curr_val % 2 == 0:
#     #             curr_val = curr_val // 2
#     #         # If value is odd 
#     #         else:
#     #             curr_val = curr_val * 3 + 1

#     #         print(all_values)
#     #         print("curr_val" + str(curr_val))
            
#     #         while curr_val not in all_values:
#     #             print(curr_val)
#     #             all_values.append(curr_val)

#     #             # if curr_val not in max_lifetime_history:
#     #             #     max_lifetime_history[curr_val] = curr_val

#     #             if curr_val > max:
#     #                 max = curr_val
#     #                 # max_lifetime_history[curr_val] = max

#     #                 for num in all_values:
#     #                     max_lifetime_history[num] = max
                
#     #             if curr_val % 2 == 0:
#     #                 curr_val = curr_val // 2
#     #             # If value is odd 
#     #             else:
#     #                 curr_val = curr_val * 3 + 1
            


#     #         # while curr_val > max:
#     #         #     max = curr_val

#     #         #     if curr_val % 2 == 0:
#     #         #         curr_val /= 2
#     #         #     # If value is odd 
#     #         #     else:
#     #         #         curr_val = curr_val * 3 + 1


            
#     #         max_lifetime_history[each_val] = max
#     #         result.append(max)
        
#     #     else:
#     #         result.append(max_lifetime_history[each_val])
    
#     return result
def max_lifetime(data_input):
    # print(data_input)
    # print(len(data_input))
    tracker_dict = {}
    result = []

    # Empty, return
    if data_input == []:
        return data_input

    for list in data_input:
        temp = []
        for element in list:
            
            # Case 1: number that can mod 8, automatically retains the same value
            if element % 8 == 0:
                tracker_dict[element] = element
                temp.append(element)

            # Case 2: number that mod (number/2)

            # if even number, check dict; 
            elif element/2 not in tracker_dict:
                counter = 0
                highestPrice = 0
                currentPrice = element
                while counter < 10:
                    if currentPrice % 2 == 0:
                        currentPrice = currentPrice//2
                    else:
                        currentPrice = currentPrice * 3 + 1

                    if currentPrice > highestPrice:
                        highestPrice = currentPrice
                    counter += 1
                temp.append(highestPrice)
                tracker_dict[element] = highestPrice

            else:
                temp.append(tracker_dict[int(element/2)])

        result.append(temp)
        temp = []
    return result

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    logging.info("data sent for evaluation ")

    # logging.info("data size: " + str(len(data)))
    # logging.info("data sent for evaluation {}".format(data))
    # stream = data.get("stream")
    result = max_lifetime(data)

    # result = max_lifetime(json.loads(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

# Test Cases

'''
---- Test Case 1 ----
Input: [[ 1, 2, 3, 4, 5 ]]
Expected output: [[ 4, 4, 16, 4, 16 ]]

---- Test Case 2 ----
Input: [[ 6, 7, 8, 9, 10 ]]
Expected output: [[ 16, 52, 16, 52, 16 ]]

---- Test Case 3 ----
Input: [
  [ 1, 2, 3, 4, 5 ],
  [ 6, 7, 8, 9, 10 ]
]

Expected output: [
  [ 4, 4, 16, 4, 16 ],
  [ 16, 52, 8, 52, 16 ]
]
'''