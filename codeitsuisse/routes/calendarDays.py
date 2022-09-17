import logging
import json
import calendar

from flask import request, jsonify
import datetime

from codeitsuisse import app

def getCalendarDays(input: list):

    # Assumption: Ignore any values less than 1 or greater than number of days of the year
    # Result Condition: 96-character case sensitive string, with every 8 characters corresponding to the month of the year starting with january
    ## "weekend,weekday, t     ,alldays,alldays,alldays,alldays,alldays,alldays,alldays,alldays,       ,"

    # mon - 0, tues - 1, wed - 2, thurs - 3, friday - 4, sat - 5, sun - 6
    # need to account for leap year where instead of 365 days, there is 366 days
    template = [
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
        [" "," "," "," "," "," "," "], 
    ]

    numOfDaysInYear = 365

    # Case 1: No days, return "       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
    if len(input) == 1:
        return "       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"

    
    # Check if leap year
    if (calendar.isleap(input[0])):
        numOfDaysInYear = 366
    
    inputWithoutYear = input[1::].sort()

    

    for i in range(len(inputWithoutYear)):
        dayOfYear = inputWithoutYear[i]
        # print("Day of Year", dayOfYear)

        # IF dayOfYear > 0 and dayOfYear < 366
        if dayOfYear > 0 and dayOfYear <= numOfDaysInYear:

            # Find the month, d.month
            yearAndDayOfYear = str(input[0]) + " " + str(dayOfYear)
            currentDate = datetime.datetime.strptime(yearAndDayOfYear, '%Y %j')
            # print(currentDate.month)
            # print("hhehehe", currentDate.weekday())
            template[currentDate.month - 1][currentDate.weekday()] = calendar.day_name[currentDate.weekday()][0].lower()
    
    result = ""
    for x in range(len(template)):
        # "numbers": [2022, 1]
        # Case 2: First day of 2022 = saturday, return "     s ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
        temp = "".join(template[x])

        # If length of array:
        # Equal: 7 = alldays
        if template[x] == "mtwtfss,":
            result += "alldays,"

        # Equal: 2, check if it's sat and sun, if yes = weekends
        elif template[x] == "     ss,":
            result += "weekends,"

        # Equal: 5, Check if sat and sun is not inside, if yes = weekdays
        elif template[x] == "mtwtf  ,":
            result += "weekdays,"
        
        else:
            result += temp + ','

    # case 3: All january 2022 weekends, return "weekend,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,", weekends = [sat, sun]

    # Case 4: First full weekday in February, return "       ,weekday,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
    
    return result


            





    return input

@app.route('/calendarDays', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("numbers")
    result = getCalendarDays(inputValue)
    logging.info("My result :{}".format(result))
    return json.dumps(result)