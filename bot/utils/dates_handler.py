days_in_month = {
    1: 31,
    2: None,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def date_handler(data):
    year = data['year']
    month = data['month']
    day = data['day']
    time = data['time']
    days_amount = days_in_month[month]
    if days_amount is None:
        if year % 400 == 0:
            days_amount = 29
        elif year % 100 == 0:
            days_amount = 28
        elif year % 4 == 0:
            days_amount = 29
        else:
            days_amount = 28

    days_result = []
    day = day.replace(' ','')
    day_list = day.split(',')
    for days in day_list:
        if (days[0] == '-' or days[-1] == '-'):
            if days[0] == '-':
                days_start = 1
                if days == '-':
                    days_end = days_amount
                else:
                    days_end = min(int(days[1:]), days_amount)
            if days[-1] == '-' and days != '-':
                days_start = int(days[:-1])
                days_end = days_amount
            flag = True
        elif '-' in days:
            days_list_start_end = days.split('-')
            days_start = int(days_list_start_end[0])
            days_end = min(int(days_list_start_end[1]),days_amount)
            flag = True
        else:
            days_result.append(int(days))
        if flag:
            for smt in range(days_start, days_end + 1):
                days_result.append(smt)
            flag = False
    days_result = list(set(days_result))


    time_result = []
    time = time.replace(' ','')
    time_list = time.split(',')
    for times in time_list:
        if times == '-':
            time_start = 0
            time_end = 24
            flag = True
        elif '-' in times:
            if times[0] == '-':
                time_start = 0
                time_end = min(int(times[1:]),24)
            elif times[-1] == '-':
                time_end = 24
                time_start = int(times[:-1])
            else:
                time_start_end = times.split('-')
                time_start = int(time_start_end[0])
                time_end = min(int(time_start_end[1]),24)
            flag = True
        else:
            time_result.append(int(times))

        if flag:
            for smt in range(time_start, time_end + 1):
                time_result.append(smt)
            flag = False
    time_result = list(set(time_result))

    result = {'year': year, 'month': month, 'day': days_result, 'time': time_result}
    return result

