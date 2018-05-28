
from datetime import datetime
import openpyxl
import member
import paths

# Antal dagar tillbaks i tiden som sparas i loggbok online.
days_saved_online = 21
latest_save = datetime.now()
data_logging = True


# Om det finns en loggbok online så laddas den in, annar skapas en ny.
try:
    loggbok = openpyxl.load_workbook(paths.xlsx_logg_online)
    loggSheet = loggbok.active
except:
    loggbok = openpyxl.Workbook()
    loggSheet = loggbok.active
    loggSheet['A1'] = 'Datum'
    loggSheet['B1'] = 'Namn'
    loggSheet['C1'] = 'Incheckning'
    loggSheet['D1'] = 'Utcheckning'
    loggSheet['E1'] = 'Anmärkning'

# Initierar medlemsregistret. Om den misslyckas så skrivs det ut i konsolen
def initMemberRegister():
    try:
        medreg = openpyxl.load_workbook(paths.xlsx_member_register)
        medSheet = medreg[medreg.sheetnames[0]]
        for row in range(2, medSheet.max_row + 1):
            keyCard = medSheet['A' + str(row)].value
            name =  medSheet['B' + str(row)].value
            board_member = medSheet['C' + str(row)].value == 'Styret'
            member.Member(keyCard, name, board_member)
    except:
        print("Could not find member register.\n" +
              "Please place the member register in the following folder\n" + 
              paths.xlsx_member_register)


# Rensar loggbok online från inloggningar som är äldre än days_saved_online
def cleanEarliestLoggbook(self):
    date_today = datetime.now()
    removed_rows = 0
    for row in range(2, loggSheet.max_row):
        time = loggSheet['A'+str(row)].value
        if time == None or \
        (date_today - strptime(time,"%Y-%m-%d")).days > days_saved_online:
            loggSheet.delete_rows(row-idx_removed, 1)
            idx_removed = idx_removed + 1

# Sparar ned loggboken på fil
def save():
        loggbok.save(paths.xlsx_logg_online)
        global latest_save
        latest_save = datetime.now()
        # ERROR ERROR ERROR FIX THIS
        #current_month = datetime.now().strftime('%Y%B')
        #loggbok.save('%s%s.xlsx' %(paths.xlsx_datalogger, current_month))
        

# Parser för att kodläsaren i verkstaden läser 24 bitar medan den på kontoret
# läser 32 bitar. Så länge kodläsaren på kontoret läser mer än 24 bitar så
# parsas denna data korrekt
def cardreaderParser(cardkey_str):
    cardreader_bits = 24
    cardkey_binary = bin(int(cardkey_str))[2:]
    cardkey_binary_appended = '0'*cardreader_bits + cardkey_binary
    return ('0,%i' %int(cardkey_binary_appended[-cardreader_bits:], 2))

# Importerar nya medlemmar från separat register. Om filen inte finns
# så skapas den. När medlemmarna skrivits in i medlemsdatabasen så
# töms filen med nya medlemmar.
def importNewMembers():
    try:
        medreg = openpyxl.load_workbook(paths.xlsx_new_members)
        medSheet = medreg[medreg.sheetnames[0]]
        for row in range(2, medSheet.max_row + 1):
            keyCard = cardreaderParser(medSheet['A' + str(row)].value)
            name =  medSheet['B' + str(row)].value
            board_member = medSheet['C' + str(row)].value == 'Styret'
            member.Member(keyCard, name, board_member)
        medreg.close()
    except:
        pass
    medreg = openpyxl.Workbook()
    medSheet = medreg.active
    medSheet.title = 'Nya medlemmar'
    medSheet['A1'] = 'Nyckelnr'
    medSheet['B1'] = 'Namn'
    medSheet['C1'] = 'Styrelsemedlem'
    medreg.save(paths.xlsx_new_members)
    medreg.close()
    saveMemberlistToFile()

# Spara den aktiva medlemslistan till fil
def saveMemberlistToFile():
    medreg = openpyxl.Workbook()
    medSheet = medreg.active
    medSheet.title = 'Medlemsregister'
    medSheet['A1'] = '0,Nyckelnr'
    medSheet['B1'] = 'Namn'
    medSheet['C1'] = 'Styrelsemedlem'
    row = 2
    for key in member.Member.member_register:
        members = member.Member.member_register[key]
        medSheet['A' + str(row)] = members.key_card
        medSheet['B' + str(row)] = members.name
        if members.board_member:
            medSheet['C' + str(row)] = 'Styret'
        else:
            medSheet['C' + str(row)] = None
        row += 1
    medreg.save(paths.xlsx_member_register)
    medreg.close()

# Sparar alla incheckade som glömde checka ut
def saveAllCheckedinToLog():
    for key in member.Member.checked_in_members:
        row = str(loggSheet.max_row + 1)
        members = member.Member.checked_in_members[key]
        loggSheet['A' + row] = members.getCheckinDate()
        loggSheet['B' + row] = members.getName()
        loggSheet['C' + row] = members.getCheckedInTime()
        loggSheet['E' + row] = 'Did not checkout'
    for key in member.Member.checked_in_styret:
        row = str(loggSheet.max_row + 1)
        members = member.Member.checked_in_styret[key]
        loggSheet['A' + row] = members.getCheckinDate()
        loggSheet['B' + row] = members.getName()
        loggSheet['C' + row] = members.getCheckedInTime()
        loggSheet['E' + row] = 'Did not checkout'
    save()

# Sparar en medlem i den aktiva loggboken (obs. sparas
# inte till excelfilen automatiskt. Detta görs i funktionen
# save)
def saveToLog(member):
    print(member)
    time_now_str = datetime.now().strftime("%H:%M:%S")
    row = str(loggSheet.max_row + 1)
    loggSheet['A' + row] = member.getCheckinDate()
    loggSheet['B' + row] = member.getName()
    loggSheet['C' + row] = member.getCheckedInTime()
    loggSheet['D' + row] = time_now_str
    # Om medlemmen checkar ut efter 00:00 så noteras det
    if time_now_str < member.getCheckedInTime():
        loggSheet['E' + row] = "Late checkout"


# Här kommer statistikdefinitioner komma.
# Ska sparas: anonymiserad data där antal unika
# besökare loggas, inloggade halvtima för halvtimma
# mellan 18:00 - 00:00 på vardagar, 06:00 - 24 på helger
# skilja mellan styret och vanliga medlemmar
# spara denna data dagligen i olika filer för varje månad
# 
def saveStatistics():
    today = datetime.now()
    try:
        statistics = openpyxl.load_workbook(paths.xlsx_statistics + today.strftime('%Y%B'))
        stat_sheet = statistics.active
    except:
        statistics = openpyxl.Workbook()
        stat_sheet = statistics.active
        stat_sheet['A1'] = 'Unika besökare'
        stat_sheet['B1'] = 'Totalt antal timmar i verkstaden'
        stat_sheet['C1'] = 'Styret antal timmar i verkstaden'
        stat_sheet['D1'] = 'Antal incheckningar totalt'
        #stat_sheet['E1'] = 'Tid med högst beläggning per halvtimma'


    row = stat_sheet.max_row
    stat_sheet['A' + row] = countUniqueVisitors()
    stat_sheet['B' + row] = countTotalHours()
    stat_sheet['C' + row] = countTotalHoursStyret()
    stat_sheet['D' + row] = countTotalCheckins()
    #stat_sheet['E' + row] = findTimeMostMembers()



     
