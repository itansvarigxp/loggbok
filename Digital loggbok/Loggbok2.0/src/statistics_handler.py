from datetime import datetime, date, timedelta
from math import sqrt
from collections import OrderedDict
import member
from excel_handler import ascii_sheet

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


statistics_categories = OrderedDict([('Unika besökare idag', uniqueVisitorsToday),
                         ('Unika besökare denna månad', uniqueVisitorsMonth),
                         ('Totalt antal timmar i verkstaden idag', totalTimeToday),
                         ('Styret antal timmar i verkstaden idag', totalTimeTodayStyret),
                         ('Totalt antal timmar i verkstaden denna månad', totalTimeMonth),
                         ('Styret antal timmar i verkstaden denna månad', totalTimeMonthStyret),
                         ('Antal incheckningar totalt idag', checkinsToday),
                         ('Genomsnittlig daglig verksamhet', dailyMean),
                         ('Standardavvikelse', dailyStdDev),
                         ('Genomsnittlig tid i verkstaden', monthlyMean),
                         ('Standardavvikelse', monthlyStdDev),
                         ('Styret genomsnittlig tid i verkstaden', monthlyMeanStyret),
                         ('Styret Standardavvikelse', monthlyStdDevStyret),
                         ('Glömda utcheckningar', member.Member.nbrCheckedInNow)])

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

def saveStatistics():
    today = date.today()
    current_date = today.strftime('%m/%d')
    current_month = today.strftime('%b')
    try:
        statistics = openpyxl.load_workbook(paths.xlsx_statistics + today.strftime('%Y%B'))
        stat_sheet = statistics.active
    except:
        statistics = openpyxl.Workbook()
        stat_sheet = statistics.active
        index = 0
        for ordered_key in statistics_categories:
            stat_sheet[ascii_sheet[i]+'1'] = ordered_key
            index += 1
    row = str(stat_sheet.max_row + 1)
    index = 0
    for ordered_key in statistics_categories:
        stat_sheet[ascii_sheet[i]+row] = statistics_categories[ordered_key]()

    if unique_visitors_this_month['CURRENTMONTH'] != current_month:
        resetMonth()
    if unique_visitors_today['CURRENTDAY'] != current_date:
        resetToday()
    stat_sheet.save('%s%s.xlsx' %(paths.xlsx_statistics, today.strftime('%Y%B')))




# def uniqueVisitors():
#     global unique_visitors_this_month
#     global unique_visitors_today
#     today = datetime.now()
#     current_date = today.strftime('%m%d')
#     current_month = today.strftime('%B')
#     visitors = {'month':len(unique_visitors_this_month),
#                 'today': len(unique_visitors_today)}
#     if not (unique_visitors_today['CURRENTDAY'] == current_date):
#         unique_visitors_today = {'CURRENTDAY': current_date}
#     if unique_visitors_this_month['CURRENTMONTH'] == current_month:
#         return visitors
#     else:
#         unique_visitors_this_month = {'CURRENTMONTH': current_month}
#         return visitors



# Här kommer statistikdefinitioner komma.
# Ska sparas: anonymiserad data där antal unika
# besökare loggas, inloggade halvtima för halvtimma
# mellan 18:00 - 00:00 på vardagar, 06:00 - 24 på helger
# skilja mellan styret och vanliga medlemmar
# spara denna data dagligen i olika filer för varje månad
# 
# def logger():
#     try:
#         logger = openpyxl.load_workbook(paths.xlsx_statistics + today.strftime('%Y%B') + '_logger')
#         logger_sheet = logger.active
#     except:
#         logger = openpyxl.Workbook()
#         logger_sheet = logger.active
#         for i in range(0,2*24)
#         logger_sheet[ascii_sheet[i] + '1'] = 

# def saveStatistics():



#     row = stat_sheet.max_row
#     stat_sheet['A' + row] = countUniqueVisitors()
#     stat_sheet['B' + row] = countTotalHours()
#     stat_sheet['C' + row] = countTotalHoursStyret()
#     stat_sheet['D' + row] = countTotalCheckins()
#     #stat_sheet['E' + row] = findTimeMostMembers()



     