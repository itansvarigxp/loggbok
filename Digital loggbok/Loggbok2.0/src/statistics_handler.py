from datetime import datetime, date, timedelta
from math import sqrt
import member

# Initierar olika variabler som används för statistikföring. Styret
# loggas både tillsammans med medlemmar och för sig.
unique_visitors_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                              'TOTALTIME': timedelta(0)}
unique_visitors_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                         'TOTALTIME': timedelta(0)}
unique_styret_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                       'TOTALTIME': timedelta(0)}
unique_styret_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                            'TOTALTIME': timedelta(0)}
# Förinsatta nycklar i dictionary är 2 stycken. Dessa är nycklar om inte
# tillhör ett kortnummer                    
preset_values = len(unique_visitors_today)
excluded_keys = ['CURRENTMONTH', 'TOTALTIME', 'CURRENTDAY']
checkin_members = 0
checkin_styret = 0

# Returnerar antalet unika besökare för dagen
def uniqueVisitorsToday():
    return len(unique_visitors_today) - preset_values + \
           len(unique_styret_today) - preset_values

# Returnerar antalet unika besökare denna månad
def uniqueVisitorsMonth():
    return len(unique_visitors_this_month) - preset_values + \
           len(unique_styret_this_month) - preset_values

# Returnerar antalet incheckningar idag
def checkinsToday():
    return checkin_members + checkin_styret

# Resetar checkinvariablerna till 0
def resetCheckins():
    global checkin_styret
    global checkin_members
    checkin_members = 0
    checkin_styret = 0

# Ökar checkin med 1
def tickCheckInsMember():
    global checkin_members
    checkin_members += 1

# Ökar styrets checkin med 1
def tickCheckInsStyret():
    global checkin_styret
    checkin_styret += 1

# Returnerar antalet inloggade just nu. Om denna kallas efter klockan
# 00:00 så kan dessa ses som att de glömt checka ut
def forgottenCheckOuts():
    return member.Member.nbrCheckedInNow()

# Retrurnerar total antal tid som spenderats i verkstaden idag
def totalTimeToday():
    return unique_visitors_today['TOTALTIME']

# Returnerar total antal tid som styret spenderat i verkstaden idag
def totalTimeTodayStyret():
    return unique_styret_today['TOTALTIME']

# Returnerar total antal tid som spenderats i verkstaden hittills denna månad
def totalTimeMonth():
    return unique_visitors_this_month['TOTALTIME']

# Returnerar total antal tid som spenderats i verkstaden av styret hittills
# denna månad
def totalTimeMonthStyret():
    return unique_styret_this_month['TOTALTIME']

# När en medlem checkar ut så uppdateras alla variabler relaterade till timetracking
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

# Om en medlem måste föra över information till ett nytt kort så kopplas
# medelmmens gamla data till det nya kortet
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

# Funktion för att räkna ut medeltalet av tiden som spenderats i verkstaden
def calcMean(total_time, N):
    try:
        mean = total_time / N
    except:
        mean = 0
    return mean

# Funktion för att räkna ut standardavvikelsen över tiden som spenderas i
# verkstaden
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

# Räknar ut det dagliga medelvärdet av antal timmar som varje medlem spenderar
# i verkstaden
def dailyMean():
    return calcMean(unique_visitors_today['TOTALTIME'],
                    len(unique_visitors_today) - preset_values)

# Räknar ut det månatagliga medelvärdet av antal timmar som varje medlem spenderar
# i verkstaden
def monthlyMean():
    return calcMean(unique_visitors_this_month['TOTALTIME'],
                    len(unique_visitors_this_month) - preset_values)

# Räknar ut det månatagliga medelvärdet som styret spenderar i verkstaden
def monthlyMeanStyret():
    return calcMean(unique_styret_this_month['TOTALTIME'],
                    len(unique_styret_this_month) - preset_values)

# Räknar ut standardavvikelsen för styret månadsvis
def monthlyStdDevStyret():
    expected_value = monthlyMeanStyret()
    N = len(unique_styret_this_month) - preset_values
    return calcStd(unique_styret_this_month, N, expected_value)

# Standardavvikelsen för alla medlemmar månadsvis
def monthlyStdDev():
    expected_value = monthlyMean()
    N = len(unique_visitors_this_month) - preset_values
    return calcStd(unique_visitors_this_month, N, expected_value)

# Standardavvikelsen för alla medlemmar dagligen
def dailyStdDev():
    expected_value = dailyMean()
    N = len(unique_visitors_today) - preset_values
    return calcStd(unique_visitors_today, N, expected_value)

# Resetar listan för unika besökare denna månaden
def resetMonth():
    global unique_visitors_this_month
    global unique_styret_this_month
    unique_visitors_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                              'TOTALTIME': timedelta(0)}
    unique_styret_this_month = {'CURRENTMONTH': date.today().strftime('%b'), \
                            'TOTALTIME': timedelta(0)}

# Resetar listan för unika besökare dagligen
def resetToday():
    global unique_styret_today
    global unique_visitors_today
    unique_visitors_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                             'TOTALTIME': timedelta(0)}
    unique_styret_today = {'CURRENTDAY': date.today().strftime('%d/%m'), \
                           'TOTALTIME': timedelta(0)}






     