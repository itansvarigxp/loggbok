

from member import *
import excel_handler as XlsxHandler
import gui_module as GUI
from datetime import datetime, timedelta
import sys


message_update_time_short = 2
message_update_time_long = 5
time_to_wait = 5
latest_message_time = datetime.now()


def exit_program():
    sys.exit()

def second_counter(datetime_wait_until):
    return str(int((datetime_wait_until - datetime.now()).seconds) + 1)

# Funktion för att flytta bilder som används till hemsidan
def mv_incheckade_png():
    nbr_checked_in_members = len(Member.checked_in_members)
    nbr_checked_in_styret = len(Member.checked_in_styret)
    if nbr_checked_in_members < 11:
        copyfile('/mnt/www/incheckade/' + nbr_checked_in_members + '.png',
                    '/mnt/www/incheckade/incheckade.png')
    else:
        copyfile('/mnt/www/incheckade/fler.png','/mnt/www/incheckade/incheckade.png')
    if nbr_checked_in_styret < 11:
        copyfile('/mnt/www/incheckade/' + nbr_checked_in_styret + '.png',
                    '/mnt/www/incheckade/styret.png')
    else:
        copyfile('/mnt/www/incheckade/fler.png','/mnt/www/incheckade/styret.png')


def timed_functions():
    #Funktioner som körs inom bestämda tidsintervall varje dygn.

    time_now = datetime.now() 
    time_now_str = time_now.strftime("%H:%M:%S")

    if  time_now_str >= ('04:00:00') and \
        time_now_str <= ('05:00:10') and \
        (XlsxHandler.latest_save + timedelta(hours = 2) < time_now): 
        #Mellan 4 och 5 på morgonen rensas loggboken, de som fortfarande är
        #incheckade blir sparade. Nya medlemmar importeras till medlemsregistret
        message_string = "Updating registers, please hold..."
        GUI.message(message_string) 
        XlsxHandler.clean_earliest_loggbook()
        XlsxHandler.import_new_members()
        XlsxHandler.save_memberlist_to_file()
        XlsxHandler.save_all_members()
        XlsxHandler.save()
        Member.clearCheckedIn()
        XlsxHandler.init_member_register()
        GUI.message("Please swipe your card")
        

commands = {
    'exit' : exit_program,
    'clear' : Member.clearCheckedIn,
    'save' : XlsxHandler.save,
    'update' : XlsxHandler.init_member_register,
    'save_all_members_to_log' : XlsxHandler.save_all_checkedin_to_log,
    'save_memberlist_to_file' : XlsxHandler.save_memberlist_to_file,
    'import_new_members' : XlsxHandler.import_new_members
}


# Initierar excelfiler
XlsxHandler.init_member_register()

while True:
    # Gör om klassvariablerna i Members till en lista av strings med namm
    # samt uppdaterar GUI-modulen som hanterar de olika listorna.
    member_str = Member.checkedInMembersToStr(16)
    styret_str = Member.checkedInStyretToStr(12)
    GUI.update_lists(styret_str,'styret_names')
    GUI.update_lists(member_str,'member_names')
    # Flagga för att förhindra för många functioncalls i whileloopen nedan.
    flag = True
    # Flytta bilder för hemsidan
#    mv_incheckade_png()
    # Denna körs så länge inget nytt input har tillkommit
    while not GUI.has_lines():
        timed_functions()
        date_time_now = datetime.now()
        if (flag and (GUI.latest_message_time < date_time_now)):
            GUI.message("Please swipe your card")
            flag = False

    # Nytt input har tillkommit
    card_number = GUI.read_input()

    if card_number in commands:
        # Om det var ett av specialkommandon i variabeln commands, kör
        # funktionen
        func = commands[card_number]
        func()
    else:
        # Annars var det en medlem som checkade in. Spara numret parsat
        # med 0, som i excelfilen
        card_number = '0,' + card_number
        time_now_str = date_time_now.strftime("%H:%M:%S")
        date_now_str = date_time_now.strftime("%Y-%m-%d")
        # Antingen var det en incheckad medlem eller inte. Var medlemmen
        # incheckad redan så checkas denne ut av klassmetoden checkout
        name = Member.checkOut(card_number)
        if name != None:
            # Om checkOut returnerar ett namn
            GUI.message('Goodbye %s' %name, 2)
            # Spara den aktuella loggboken i excel
            XlsxHandler.save()

        elif card_number in Member.member_register:
            # checkOut returnerade None och numret fanns i medlemsregitret
            # Spara medlemsobjektet lokalt och checka in det.
            member_local = Member.member_register[card_number]
            Member.checkIn(member_local)
            GUI.message('Welcome %s' %member_local.getName(), 2)

            # Beroende på om det är en styrelsemedlem eller ej så uppdateras
            # antingen texten tillhörande medlemmar eller den tillhörande
            # styret
            if (member_local.getBoardmember()):
                GUI.update_lists(Member.toListStr(Member.checked_in_styret, 12),
                                 'styret_names')
            else:
                GUI.update_lists(Member.toListStr(Member.checked_in_members, 16), 
                                 'member_names')
        # Om kortnumret inte finns sparat i medlemsdatabasen, initiera bytesprocessen
        else:
            old_card_number = card_number
            date_time_to_wait = datetime.now() + timedelta(0,time_to_wait)

            # Avbryts antingen om tiden går ut eller om ett nytt kort scannas
            while (not GUI.has_lines()) and (date_time_to_wait > datetime.now()):
                message_string = ("Card not recognised!\nPlease scan again to start a transfer\n"
                                  "process, or wait %s seconds to cancel"
                                  %second_counter(date_time_to_wait))
                GUI.message(message_string)
            # Om samma kort scannades
            if (GUI.has_lines()):
                new_card_number = '0,' + GUI.read_input()
                if new_card_number == old_card_number:
                    date_time_to_wait = datetime.now() + timedelta(0,time_to_wait)

                    # Avbryts antingen om tiden går ut eller om ett nytt kort scannas
                    while (not GUI.has_lines()) and (date_time_to_wait > datetime.now()):
                        message_string = ("Now scan your old card that you want to"
                                          " transfer\nyour data from, or wait %s seconds to"
                                          "cancel" %second_counter(date_time_to_wait))
                        GUI.message(message_string)
                    # Om ett nytt kort scannades och det gamla kortet finns i databasen
                    # så bytes det ut
                    if GUI.has_lines():
                        old_card_number = '0,' + GUI.read_input()
                        
                        if old_card_number in Member.member_register:
                            local_member = Member.member_register[old_card_number]
                            local_member.changeKeyCard(new_card_number)
                            XlsxHandler.save_memberlist_to_file()
                        else:
                            message_string = ("Old card not in member database..."
                                              "\nTransfer failed.")
                            GUI.message(message_string, message_update_time_long)
                    else:
                        message_string = "Aborted!"
                        GUI.message(message_string, message_update_time_short)
                        GUI.remove_input()
                else:
                    message_string = "Aborted!"
                    GUI.message(message_string, message_update_time_short)
                    GUI.remove_input()
            else:
                message_string = "Aborted!"
                GUI.message(message_string, message_update_time_short)
                GUI.remove_input()

