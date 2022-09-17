import logging
import json

from flask import request, jsonify

from codeitsuisse import app

def quordle_part_1(answers, attempts):
    leftovers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wrong_tries = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "H": 0,
        "I": 0,
        "J": 0,
        "K": 0,
        "L": 0,
        "M": 0,
        "N": 0,
        "O": 0,
        "P": 0,
        "Q": 0,
        "R": 0,
        "S": 0,
        "T": 0,
        "U": 0,
        "V": 0,
        "W": 0,
        "X": 0,
        "Y": 0,
        "Z": 0
    }

    all_answers = ''.join(answers)
    # all_attempts = ''.join(answers)

    # for each_attempt in attempts:
    #     # each_attempt = set(each_attempt)
    #     print(each_attempt)
    #     for ch in each_attempt:
    #         print(ch)
    #         if ch not in all_answers:
    #             wrong_tries[ch] += 1
    #         else:
    #             # index = all_answers.index(ch)
    #             all_answers = all_answers.replace(ch, '', 1)
    #         print(all_answers)
    #     print(wrong_tries)

    each_attempt_wrong = []
    wrong_guess = ""
    for each_attempt in attempts:
        print("all_answers: " + all_answers)
        each_attempt = set(each_attempt)
        print(each_attempt)

        for ch in each_attempt:
            # print(ch)
            leftovers = leftovers.replace(ch, '', 1)
            if ch not in all_answers:
                # wrong_tries[ch] += 1
                if ch not in wrong_guess:
                    wrong_guess += ch
            else:
                # index = all_answers.index(ch)
                all_answers = all_answers.replace(ch, '', 1)
                if ch not in all_answers:
                    wrong_guess += ch
                    # each_attempt_wrong.append("ch")

        print("wrong_guess: " + wrong_guess)
        each_attempt_wrong.append(wrong_guess)
        print(each_attempt_wrong)
        print()

    for each_letter in (''.join(each_attempt_wrong)):
        wrong_tries[each_letter] += 1

    print(wrong_tries)

    
    # Aggregate into string
    result = ""
    for try_num in wrong_tries.values():
        if try_num != 0:
            result += str(try_num)

    return (result, leftovers)

def quordle_part_2(numGrey, leftovers, numbers):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ''
    print("numGrey: " + numGrey)
    print("leftovers: " + leftovers)

    for i in range(0, 21, 5):
        current_list = numbers[i:(i+5)]
        print(current_list)
        binary = ''
        for num in current_list:
            if str(num) in numGrey:
                binary += '1'
            else:
                binary += '0'

        decimal = int(binary, 2)
        result += letters[decimal - 1]

    return (result + leftovers)
    



@app.route('/quordleKeyboard', methods=['POST'])
def quordleKeyboard():
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

# Test Cases

'''
---- Test Case 1 ----
Input: {
  "answers": ["ABCDE", "FGHIJ", "KLMNO", "PQRST"],
  "attempts": ["XYZXY", "ABCDE", "FGHIJ", "AAAAA", "PQRST", "KLMNO"],
  "numbers": [125, 441, 968, 137, 417, 554, 978, 666, 145, 137, 343, 26, 898, 54, 222, 2, 777, 837, 6, 478, 970, 526, 26, 44, 41]
}
Expected output: {"part1": "55555444441111122222666", "part2": "HTKRGUVW"}

---- Test Case 2 ----
Input: {
  "answers": ["VVIDH", "MZLPS", "BPCYN", "XYGGM"],
  "attempts": ["JKGJB", "ZGRUJ", "XYGGM", "BPCYN", "MHXGE", "DZENT", "ZXWQW", "VVIDH", "MZLPS"],
  "numbers": [125, 441, 968, 137, 417, 554, 978, 666, 145, 137, 343, 26, 898, 54, 222, 2, 777, 837, 6, 478, 970, 526, 26, 44, 41]
}
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