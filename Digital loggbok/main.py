

import member
import excel_handler
import gui
import datetime

# initiera
# yttre loop
# inre loop
# default message



# Start of main here
message_update_time_short = 2
message_update_time_long = 5
latest_message_time = datetime.datetime.now()

# Bakgrundsloop som uppdaterar loggboken vid behov
# samt tömmer loggboken vid ett visst klockslag

def exit_program():
    sys.exit()


def second_counter(datetime_wait_until):
    return str(int((datetime_wait_until - datetime.datetime.now()).seconds) + 1)



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
    time_now = datetime.datetime.now()  # kolla klockan
    time_now_str = time_now.strftime("%H:%M:%S")
    if  time_now_str >= ('04:00:00') and \
        time_now_str <= ('05:00:10') and \
        (XlsxHandler.latest_save + datetime.timedelta(hours = 2) < time_now) :  # Mellan 4 & 5
        # Show message initializing databases, please hold

        XlsxHandler.clean_earliest_loggbook()
        XlsxHandler.import_new_members()
        XlsxHandler.save_memberlist_to_file()
        XlsxHandler.save_all_members()
        XlsxHandler.save()
        Member.clearCheckedIn()
        XlsxHandler.init_member_register()
        

commands = {
    # 'exit' : exit_program,
    # 'clear' : Member.clearCheckedIn, # finns ej
    # 'save' : XlsxHandler.save, # finns ej
    # 'update' : XlsxHandler.init_member_register, # finns ej
    # 'save_all_members' : XlsxHandler.save_all_members, # finns ej
    # 'save_memberlist_to_file' : XlsxHandler.save_memberlist_to_file, # finns ej
    # 'import_new_members' : XlsxHandler.import_new_members # finns ej
}




gui_object = gui.LoggbookGUI()
xlsx_object = excel_handler.XlsxHandler()



while True:
    member_str = member.Member.checkedInMembersToStr(16)
    styret_str = member.Member.checkedInStyretToStr(12)
    gui_object.update_lists(styret_str,'styret_names')
    gui_object.update_lists(member_str,'member_names')
    flag = True
#    mv_incheckade_png()
    while not gui_object.has_lines():
        timed_functions()
        date_time_now = datetime.datetime.now()
        if (flag and (gui_object.latest_message_time < date_time_now)):
            gui_object.message("Please swipe your card")
            flag = False

    card_number = gui_object.read_input()
    if card_number in commands:
        func = commands[card_number]
        func()
    else:
        card_number = '0,' + card_number
        # Number was read
        time_now_str = date_time_now.strftime("%H:%M:%S")
        date_now_str = date_time_now.strftime("%Y-%m-%d")

        name = member.Member.checkOut(card_number)
        if name != None:
            gui_object.message('Goodbye %s' %name, 2)
            # spara i loggboken
        elif card_number in member.Member.member_register:
            member_local = member.Member.member_register[card_number]
            member.Member.checkIn(member_local)
            gui_object.message('Welcome %s' %member_local.getName(), 2)
            print(member.Member.checked_in_styret)
            print(member.Member.checked_in_members)
            if (member_local.getBoardmember()):
                gui_object.update_lists(member.Member.toListStr(member.Member.checked_in_styret, 12), 'styret_names') # bugg i to string
            else:
                gui_object.update_lists(member.Member.toListStr(member.Member.checked_in_members, 16), 'member_names')
            # då ska vi checka in
        else:
            time_to_wait = 5
            old_card_number = card_number
            date_time_to_wait = datetime.datetime.now() + datetime.timedelta(0,time_to_wait)

            while (not gui_object.has_lines()) and (date_time_to_wait > datetime.datetime.now()):
                message_string = 'Card not recognised!\nPlease scan again to start a transfer process,\nor wait %s seconds to cancel' %second_counter(date_time_to_wait)
                gui_object.message(message_string)
            
            if (gui_object.has_lines()):
                new_card_number = '0,' + gui_object.read_input()
                if new_card_number == old_card_number:
                    date_time_to_wait = datetime.datetime.now() + datetime.timedelta(0,time_to_wait)
                    while (not gui_object.has_lines()) and (date_time_to_wait > datetime.datetime.now()):
                        message_string = ('Now scan your old card that you want to transfer your data from,\nor wait %s seconds to cancel' %second_counter(date_time_to_wait))
                        gui_object.message(message_string)
                    
                    if gui_object.has_lines():
                        old_card_number = '0,' + gui_object.read_input()
                        
                        if old_card_number in member.Member.member_register:
                            member.Member.member_register[new_card_number] = member.Member.member_register[old_card_number]
                            del member.Member.member_register[old_card_number]
                            XlsxHandler.save_memberlist_to_file()
                        else:
                            message_string = ('Old card not in member database...\nTransfer failed.')
                            gui_object.message(message_string, message_update_time_long)
                    else:
                        message_string = "Aborted!"
                        gui_object.message(message_string, message_update_time_short)
                        gui_object.remove_input()
                else:
                    message_string = "Aborted!"
                    gui_object.message(message_string, message_update_time_short)
                    gui_object.remove_input()

            else:
                message_string = "Aborted!"
                gui_object.message(message_string, message_update_time_short)
                gui_object.remove_input()

