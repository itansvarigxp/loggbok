from datetime import datetime, date, timedelta
from math import sqrt
import member

unique_visitors_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                              'TOTALTIME': timedelta(0)}
unique_visitors_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                         'TOTALTIME': timedelta(0)}
unique_styret_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                       'TOTALTIME': timedelta(0)}
unique_styret_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                            'TOTALTIME': timedelta(0)}

preset_values = len(unique_visitors_today)
excluded_keys = ['CURRENTMONTH', 'TOTALTIME', 'CURRENTDAY']
checkin_members = 0
checkin_styret = 0

def uniqueVisitorsToday():
    return len(unique_visitors_today) - preset_values + \
           len(unique_styret_today) - preset_values

def uniqueVisitorsMonth():
    return len(unique_visitors_this_month) - preset_values + \
           len(unique_styret_this_month) - preset_values

def checkinsToday():
    return checkin_members + checkin_styret

def resetCheckins():
    global checkin_styret
    global checkin_members
    checkin_members = 0
    checkin_styret = 0

def tickCheckInsMember():
    global checkin_members
    checkin_members += 1

def tickCheckInsStyret():
    global checkin_styret
    checkin_styret += 1

def forgottenCheckOuts():
    return member.Member.nbrCheckedInNow()

def totalTimeToday():
    return unique_visitors_today['TOTALTIME']

def totalTimeTodayStyret():
    return unique_styret_today['TOTALTIME']

def totalTimeMonth():
    return unique_visitors_this_month['TOTALTIME']

def totalTimeMonthStyret():
    return unique_styret_this_month['TOTALTIME']

def checkOutStat(member):
    key_card = member.getKeyCardNumber()
    time_in_workshop = datetime.now() - member.getCheckInTimeObject()
    
    if member.getBoardmember:
        if key_card in unique_styret_today: 
            unique_styret_today[key_card] += time_in_workshop
        else:
            unique_styret_today[key_card] = time_in_workshop
        if key_card in unique_styret_this_month:
            unique_styret_this_month[key_card] += time_in_workshop
        else:
            unique_styret_this_month[key_card] = time_in_workshop

        unique_styret_this_month['TOTALTIME'] += time_in_workshop
        unique_styret_today['TOTALTIME'] += time_in_workshop

    if key_card in unique_visitors_today:
        unique_visitors_today[key_card] += time_in_workshop
    else:
        unique_visitors_today[key_card] = time_in_workshop
    if key_card in unique_visitors_this_month:
        unique_visitors_this_month[key_card] += time_in_workshop
    else:
        unique_visitors_this_month[key_card] = time_in_workshop
    unique_visitors_this_month['TOTALTIME'] += time_in_workshop
    unique_visitors_today['TOTALTIME'] += time_in_workshop

def changeCardStat(key_card, old_key_card):
    if old_key_card in unique_visitors_today:
        unique_visitors_today[key_card] = unique_visitors_today[old_key_card]
        del unique_visitors_today[old_key_card]
    if old_key_card in unique_visitors_this_month:
        unique_visitors_this_month[key_card] = unique_visitors_this_month[old_key_card]
        del unique_visitors_this_month[old_key_card]

    if old_key_card in unique_styret_today:
        unique_styret_today[key_card] = unique_styret_today[old_key_card]
        del unique_styret_today[old_key_card]
    if old_key_card in unique_styret_this_month:
        unique_styret_this_month[key_card] = unique_styret_this_month[old_key_card]
        del unique_styret_this_month[old_key_card]

def calcMean(total_time, N):
    try:
        mean = total_time / N
    except:
        mean = 0
    return mean

def calcStdDev(visitor_dict, N, expected_value):
    accu = timedelta(0)
    for unique_members in visitor_dict:
        if not unique_members in excluded_keys:
            accu += pow(visitor_dict[unique_members] - expected_value, 2)
    try:
        accu = sqrt(accu / N)
    except:
        accu = timedelta(0)
    return accu

def dailyMean():
    return calcMean(unique_visitors_today['TOTALTIME'],
                    len(unique_visitors_today) - preset_values)
def monthlyMean():
    return calcMean(unique_visitors_this_month['TOTALTIME'],
                    len(unique_visitors_this_month) - preset_values)

def monthlyMeanStyret():
    return calcMean(unique_styret_this_month['TOTALTIME'],
                    len(unique_styret_this_month) - preset_values)

def monthlyStdDevStyret():
    expected_value = monthlyMeanStyret()
    N = len(unique_styret_this_month) - preset_values
    return calcStd(unique_styret_this_month, N, expected_value)

def monthlyStdDev():
    expected_value = monthlyMean()
    N = len(unique_visitors_this_month) - preset_values
    return calcStd(unique_visitors_this_month, N, expected_value)

def dailyStdDev():
    expected_value = dailyMean()
    N = len(unique_visitors_today) - preset_values
    return calcStd(unique_visitors_today, N, expected_value)

def resetMonth():
    global unique_visitors_this_month
    global unique_styret_this_month
    unique_visitors_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                              'TOTALTIME': timedelta(0)}
    unique_styret_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                            'TOTALTIME': timedelta(0)}

def resetToday():
    global unique_styret_today
    global unique_visitors_today
    unique_visitors_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                             'TOTALTIME': timedelta(0)}
    unique_styret_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                           'TOTALTIME': timedelta(0)}






     