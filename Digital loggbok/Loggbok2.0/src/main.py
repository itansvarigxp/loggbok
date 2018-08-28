

from member import *
import excel_handler as XlsxHandler
import statistics_handler as StatLogger
import gui_module as GUI
from datetime import datetime, timedelta
import sys
import os

message_update_time_short = 2
message_update_time_long = 5
time_to_wait = 5
latest_message_time = datetime.now()


def exitProgram():
    sys.exit()

def secondCounter(datetime_wait_until):
    return str(int((datetime_wait_until - datetime.now()).seconds) + 1)

# Funktion för att flytta bilder som används till hemsidan
def mvIncheckadePNG():
    nbr_checked_in_members = len(Member.checked_in_members)
    nbr_checked_in_styret = len(Member.checked_in_styret)
    if nbr_checked_in_members < 11:
        copyfile(res_path + nbr_checked_in_members + '.png',
                   webpage_resources_path + 'incheckade.png')
    else:
        copyfile(res_path + 'fler.png', webpage_resources_path + 'incheckade.png')

    if nbr_checked_in_styret < 11:
        copyfile(res_path + nbr_checked_in_styret + '.png', webpage_resources_path + 'styret.png')
    else:
        copyfile(res_path + 'fler.png', webpage_resources_path + 'styret.png' )


def timedFunctions():
    #Funktioner som körs inom bestämda tidsintervall varje dygn.
    #print('in timed function')
    time_now = datetime.now() 
    time_now_str = time_now.strftime("%H:%M:%S")
    #print(time_now)
    #print((XlsxHandler.latest_save + timedelta(hours = 0, minutes = 1))
    # Debugga denna
    if  time_now_str >= ('04:00:00') and \
        time_now_str <= ('05:00:10') and \
        (XlsxHandler.latest_save + timedelta(hours = 2) < time_now): 
        #Mellan 4 och 5 på morgonen rensas loggboken, de som fortfarande är
        #incheckade blir sparade. Nya medlemmar importeras till medlemsregistret
        message_string = "Updating registers, please hold..."
        GUI.message(message_string)
        # Dagens statistik loggas. Måste göras innan de som glömt att checka ut
        # rensas ur loggboken
        XlsxHandler.saveStatistics()
        StatLogger.resetCheckins()
        XlsxHandler.cleanEarliestLoggbook()
        XlsxHandler.importNewMembers()
        XlsxHandler.saveMemberlistToFile()
        XlsxHandler.saveAllCheckedinToLog()
        XlsxHandler.save()
        Member.clearCheckedIn()
        XlsxHandler.initMemberRegister()
        member_str = Member.checkedInMembersToStr(16)
        styret_str = Member.checkedInStyretToStr(12)
        GUI.updateLists(styret_str,'styret_names')
        GUI.updateLists(member_str,'member_names')
        GUI.message("Please swipe your card")
        
# Kommandon som kan skrivas i programmet för att kalla på motsvarande funktion
commands = {
    'exit' : exitProgram,
    'clear' : Member.clearCheckedIn,
    'save' : XlsxHandler.save,
    'update' : XlsxHandler.initMemberRegister,
    'save checkedin' : XlsxHandler.saveAllCheckedinToLog,
    'save members' : XlsxHandler.saveMemberlistToFile,
    'save statistics' : XlsxHandler.saveStatistics,
    'import' : XlsxHandler.importNewMembers,
    'clean' : XlsxHandler.cleanEarliestLoggbook
}


# Initierar excelfiler
XlsxHandler.initMemberRegister()

while True:
    # Gör om klassvariablerna i Members till en lista av strings med namm
    # samt uppdaterar GUI-modulen som hanterar de olika listorna.
    member_str = Member.checkedInMembersToStr(16)
    styret_str = Member.checkedInStyretToStr(12)
    GUI.updateLists(styret_str,'styret_names')
    GUI.updateLists(member_str,'member_names')
    # Flagga för att förhindra för många functioncalls i whileloopen nedan.
    flag = True
    # Flytta bilder för hemsidan
#    mvIncheckadePNG()
    # Denna körs så länge inget nytt input har tillkommit
    while not GUI.hasLines():
        timedFunctions()
        date_time_now = datetime.now()
        if (flag and (GUI.latest_message_time < date_time_now)):
            GUI.message("Please swipe your card")
            flag = False

    # Nytt input har tillkommit
    card_number = GUI.readInput()

    if card_number in commands:
        # Om det var ett av specialkommandon i variabeln commands, kör
        # funktionen
        commands[card_number]()
    else:
        # Annars var det en medlem som checkade in. Spara numret parsat
        # med 0, som i excelfilen
        card_number = '0,' + card_number
        time_now_str = date_time_now.strftime("%H:%M:%S")
        date_now_str = date_time_now.strftime("%Y-%m-%d")
        # Antingen var det en incheckad medlem eller inte. Var medlemmen
        # incheckad redan så checkas denne ut av klassmetoden checkout
        member = Member.checkOut(card_number)
        if member != None:
            # Om checkOut returnerar ett namn
            GUI.message('Goodbye %s' %member.getName(), 2)
            # Spara den aktuella loggboken i excel
            StatLogger.checkOutStat(member)
            XlsxHandler.saveToLog(member)
            XlsxHandler.save()

        elif card_number in Member.member_register:
            # checkOut returnerade None och numret fanns i medlemsregitret
            # Spara medlemsobjektet lokalt och checka in det.
            member_local = Member.member_register[card_number]
            Member.checkIn(member_local)
            GUI.message('Welcome %s' %member_local.getName(), 2)

            #XlsxHandler.checkinUniqueLogger(card_number)
            # Beroende på om det är en styrelsemedlem eller ej så uppdateras
            # antingen texten tillhörande medlemmar eller den tillhörande
            # styret
            if (member_local.getBoardmember()):
                StatLogger.tickCheckInsStyret()
                GUI.updateLists(Member.toListStr(Member.checked_in_styret, 12), 
                                'styret_names')
            else:
                StatLogger.tickCheckInsMember()
                GUI.updateLists(Member.toListStr(Member.checked_in_members, 16), 
                                'member_names')
        # Om kortnumret inte finns sparat i medlemsdatabasen, initiera bytesprocessen
        else:
            old_card_number = card_number
            date_time_to_wait = datetime.now() + timedelta(0,time_to_wait)

            # Avbryts antingen om tiden går ut eller om ett nytt kort scannas
            while (not GUI.hasLines()) and (date_time_to_wait > datetime.now()):
                message_string = ("Card not recognised!\nPlease scan again to start a transfer\n"
                                  "process, or wait %s seconds to cancel"
                                  %secondCounter(date_time_to_wait))
                GUI.message(message_string)
            # 1 Om kort scannades
            if (GUI.hasLines()):
                new_card_number = '0,' + GUI.readInput()
                # 2 Om samma kort scannades
                if new_card_number == old_card_number:
                    date_time_to_wait = datetime.now() + timedelta(0,time_to_wait)

                    # Avbryts antingen om tiden går ut eller om ett nytt kort scannas
                    while (not GUI.hasLines()) and (date_time_to_wait > datetime.now()):
                        message_string = ("Now scan your old card that you want to"
                                          " transfer\nyour data from, or wait %s seconds to"
                                          "cancel" %secondCounter(date_time_to_wait))
                        GUI.message(message_string)
                    # 3 Om ett nytt kort scannades
                    if GUI.hasLines():
                        old_card_number = '0,' + GUI.readInput()
                        # Om det gamla kortet finns i databasen så byts det ut
                        if old_card_number in Member.member_register:
                            local_member = Member.member_register[old_card_number]
                            local_member.changeKeyCard(new_card_number)
                            # Kortet byts även ut i statistiken för att inte felaktigt registrera
                            # för många medlemmar
                            StatLogger.changeCardStat(new_card_number, old_card_number)
                            XlsxHandler.saveMemberlistToFile()

                            #changeCardUniqueLogger(new_card_number, old_card_number):
                            # Annars så meddelas användare att kortet inte finns i databasen
                        else:
                            message_string = ("Old card not in member database..."
                                              "\nTransfer failed.")
                            GUI.message(message_string, message_update_time_long)
                    # 3 Om inget kort scannades
                    else:
                        message_string = "Aborted!"
                        GUI.message(message_string, message_update_time_short)
                        GUI.removeInput()
                # 2 Om annat kort scannades
                else:
                    message_string = "Aborted!"
                    GUI.message(message_string, message_update_time_short)
                    GUI.removeInput()
            # 1 Annars avbryt
            else:
                message_string = "Aborted!"
                GUI.message(message_string, message_update_time_short)
                GUI.removeInput()

