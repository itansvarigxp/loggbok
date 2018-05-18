

import os
import tkinter as tk

import sys, openpyxl, GUI
from threading import Thread, Timer
from pyautogui import press, typewrite
from shutil import copyfile
from os import remove
import datetime, time
from time import sleep

# Fixa emeritus

class Member(object):
    
    """docstring for Member"""
    def __init__(self, key_card, name, checkin, board_member):
        self.key_card = key_card
        self.name = name
        self.checked_in = checkin
        self.board_member = board_member or False


    def getname():
        return self.name

    def getboardmember():
        return self.board_member

    def getcheckedintime():
        return self.checked_in

root = tk.Tk()
root.title("XP digital logg v2.0")
# a little more than width and height of image
main_window_width = 700
main_window_height = 800
x = 10
y = 10
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (main_window_width, main_window_height, x, y))

file_name_bg = "bg.gif"
in_file = open(file_name_bg, "rb")
data_bytes = in_file.read()
in_file.close()

photo = tk.PhotoImage(data=data_bytes)
# create a white canvas
cv = tk.Canvas(bg='white')
cv.configure(width=665, height=660)

cv.pack(side=tk.TOP, expand=False)
# put the image on the canvas with
# create_image(xpos, ypos, image, anchor)
cv.create_image(25, 25, image=photo, anchor='nw')

member_title = "Checked-in members"
styret_title = "Checked-in board members"
member_title_offsetX = 5
member_title_offsetY = 250
styret_title_offsetX = member_title_offsetX
styret_title_offsetY = 0
title_color = "black"
title_size = 36
title_font = ('Arial', title_size, 'bold')

cv.create_text(member_title_offsetX, member_title_offsetY, fill=title_color,
						 font=title_font, anchor='nw', text=member_title)

cv.create_text(styret_title_offsetX, styret_title_offsetY, fill=title_color,
						font=title_font, anchor='nw', text=styret_title)

namelist_color = "black"
namelist_size = 18
namelist_font=('Arial', namelist_size)
namelist_color = "black"
namelist_row_padding = 5
namelist_col_padding = 10
styret_namelist_offsetX = namelist_col_padding
styret_namelist_offsetY = styret_title_offsetY + namelist_row_padding + title_size
member_namelist_offsetX = namelist_col_padding
member_namelist_offsetY = member_title_offsetY + namelist_row_padding + title_size

styret_namelist = ""
member_namelist = ""

interactive_area_width = main_window_width
interactive_area_height = 80
message_area_height = 65
input_area_height = 15
message_height = message_area_height - input_area_height
message_area_width = main_window_width
message_width = message_area_width
input_area_width = message_area_width

message_area_bg_color = 'black'
message_area_fg_color = 'white'

input_area_bg_color = 'black'
input_area_fg_color = 'white'

interactive_area = tk.Frame(root, bg=message_area_bg_color, width = interactive_area_width, height = interactive_area_height)
#message_area.configure(width=700, height=text_area_height)
interactive_area.pack(side=tk.BOTTOM, expand=False)

message_area = tk.Frame(interactive_area, bg=message_area_bg_color, width = message_area_width, height = message_area_height, bd = 0)
message_area.pack(side=tk.TOP, expand = False)
message_area.pack_propagate(False)

message_variable = tk.StringVar()
message_variable.set("Please swipe your card")
message = tk.Message(message_area, bg=message_area_bg_color, width = 500, fg = message_area_fg_color, textvariable = message_variable)
message.configure(font=('Arial', 18, 'bold'))
message.pack(side=tk.TOP, expand=False)

text = tk.Text(interactive_area, height=input_area_height, width=input_area_width, 
                bg=input_area_bg_color, foreground=input_area_fg_color, bd = 0)

text.pack(side=tk.BOTTOM, expand=False)
text.focus()
# Här börjar kod
command = ''
card_number = ''
checked_in_members = {}
checked_in_members_str = ''
checked_in_styret = {}
checked_in_styret_str = ''
member_register = {}
board_members_checkedin = 0
loggbok = {}
loggSheet = {}
latest_save = datetime.datetime.now()
current_month = latest_save.strftime('%Y%B')
days_saved_online = 30
path_to_logg_online = 'Loggbok_online.xlsx'
path_to_member_register = 'Medlemsregister.xlsx'
path_to_new_members = 'Nyamedlemmar.xlsx'
path_to_datalogger = ''
#path_to_logg_online = 'info/Loggbok_online.xlsx'
#path_to_member_register = '/mnt/www/Medlemsregister.xlsx'
#path_to_new_members = '/mnt/www/Nyamedlemmar.xlsx'
#path_to_datalogger = '/mnt/www/datalog/'


def init_log():
    # set a path to this
    global loggbok
    loggbok = openpyxl.load_workbook(path_to_logg_online)
    global loggSheet
    loggSheet = loggbok.active
    #loggbok._archive.close()



def clean_earliest_loggbook():
    global loggSheet
    date_today = datetime.datetime.now()
    rows = []
    idx_removed = 0
    for row in range(2, loggSheet.max_row):
        if loggSheet['A'+str(row)].value == None:
            rows.append(row)
        else:
            date_logged = date_today.strptime(loggSheet['A'+str(row)].value,"%Y-%m-%d")
            if (date_today - date_logged).days > days_saved_online:
                rows.append(row)               
    for row in rows:
        loggSheet.delete_rows(row-idx_removed, 1)
        idx_removed = idx_removed + 1

# Spara listan externt loggbok.save('info/Loggbok_extern.xlsx')
def save():
        # set a path to this
        loggbok.save(path_to_logg_online)
        # set a path to this
        # ERROR ERROR ERROR FIX THIS
        loggbok.save('%s%s.xlsx' %(path_to_datalogger, current_month))


# Bakgrundsloop som uppdaterar loggboken vid behov
# samt tömmer loggboken vid ett visst klockslag
def timed_functions():
    time_now = datetime.datetime.now()  # kolla klockan
    time_now_str = time_now.strftime("%H:%M:%S")

    if time_now_str >= ('04:00:00') and time_now_str <= ('05:00:10') and (latest_save + datetime.timedelta(hours = 2) < time_now) :  # Mellan 4 & 5
        # Show message initializing databases, please hold
        clean_earliest_loggbook()
        import_new_members()
        save_memberlist_to_file()
        save_all_members()
        save()
        clear()
        init_member_register()
        global current_month
        current_month = datetime.now().strftime('%Y%B')

def cardreader_parser(cardkey_str):
    cardreader_bits = 24
    cardkey_binary = bin(int(cardkey_str))[-cardreader_bits:]
    return ('0,%i' %int(cardkey_binary, 2))



def import_new_members():
    # Använd bara denna på natten eller något.
    medreg = openpyxl.load_workbook(path_to_new_members)
    medSheet = medreg[medreg.sheetnames[0]]
    global member_register
    for row in range(2, medSheet.max_row + 1):
        keyCard = cardreader_parser(medSheet['A' + str(row)].value)
        name =  medSheet['B' + str(row)].value
        member_register[keyCard] = (name, medSheet['C' + str(row)].value == 'Styret')
        print(member_register[keyCard])
    medreg.close()
    medreg = openpyxl.Workbook()
    medSheet = medreg.active
    medSheet.title = 'Nya medlemmar'
    medSheet['A1'] = 'Nyckelnr'
    medSheet['B1'] = 'Namn'
    medSheet['C1'] = 'Styrelsemedlem'
    medreg.save(path_to_new_members)
    medreg.close()
    save_memberlist_to_file()

def save_memberlist_to_file():
    medreg = openpyxl.Workbook()
    medSheet = medreg.active
    medSheet.title = 'Medlemsregister'
    medSheet['A1'] = '0,Nyckelnr'
    medSheet['B1'] = 'Namn'
    medSheet['C1'] = 'Styrelsemedlem'
    row = 2
    for keyCard in member_register:
        member = member_register[keyCard]
        medSheet['A' + str(row)] = keyCard
        medSheet['B' + str(row)] = member[0]
        if member[1]:
            medSheet['C' + str(row)] = 'Styret'
    medreg.save(path_to_member_register)
    medreg.close()

def clear():
    global checked_in_members
    global checked_in_styret
    checked_in_members = {}
    checked_in_styret = {}

def members_to_str(checked_in, split_at):
    list_of_names_tmp = []
    list_of_names = []
    for keys in checked_in:
       list_of_names_tmp.append(checked_in[keys][0])
    nbr_of_elems = len(list_of_names_tmp) // split_at
    for idx in range(0, nbr_of_elems+1):
        list_of_names.append('\n'.join(list_of_names_tmp[idx*split_at:((idx+1)*split_at)-1]))
    return list_of_names

def second_counter(datetime_wait_until):
    return str(int((datetime_wait_until - datetime.datetime.now()).seconds) + 1)


def exit_program():
    sys.exit()


def update_lists():
    cv.delete('styret_names')
    cv.delete('member_names')
    next_col = 300
    checked_in_members_str = members_to_str(checked_in_members, 16)
    checked_in_styret_str = members_to_str(checked_in_styret, 10)
    idx = 0
    for items in checked_in_styret_str:
        cv.create_text(styret_namelist_offsetX + next_col*idx, styret_namelist_offsetY, 
                        fill=namelist_color, font=namelist_font, anchor='nw', text=items, tag='styret_names')
        idx = idx + 1
    
    idx = 0
    for items in checked_in_members_str:
        cv.create_text(member_namelist_offsetX + next_col*idx, member_namelist_offsetY,
                        fill=namelist_color, font=namelist_font, anchor='nw', text=items, tag='member_names')
        idx = idx + 1

def init_member_register():
    medreg = openpyxl.load_workbook(path_to_member_register)
    medSheet = medreg[medreg.sheetnames[0]]
    global member_register
    member_register = {}
    for row in range(2, medSheet.max_row + 1):
        keyCard = medSheet['A' + str(row)].value
        print(medSheet['A' + str(row)].value)
        name =  medSheet['B' + str(row)].value
        member_register[keyCard] = (name, medSheet['C' + str(row)].value == 'Styret')
    medreg.close()

def mv_incheckade_png():
    nbr_checked_in_members = len(checked_in_members)
    nbr_checked_in_styret = len(checked_in_styret)
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


def line_count(string):
    return sum(1 for char in string if char == '\n')

def save_all_members():
    for key in checked_in_members:
        global loggSheet
        member = checked_in_members[key]
        time_checkedin = member[2]
        row = str(loggSheet.max_row + 1)
        loggSheet['A' + row] = member[1] # date
        loggSheet['B' + row] = member[0] # name
        loggSheet['C' + row] = time_checkedin
    for key in checked_in_styret:
        member = checked_in_styret[key]
        time_checkedin = member[2]
        row = str(loggSheet.max_row + 1)
        loggSheet['A' + row] = member[1] # date
        loggSheet['B' + row] = member[0] # name
        loggSheet['C' + row] = time_checkedin

        



commands = {
    'exit' : exit_program,
    'clear' : clear,
    'save' : save,
    'update' : init_member_register,
    'save_all_members' : save_all_members,
    'save_memberlist_to_file' : save_memberlist_to_file,
    'import_new_members' : import_new_members
}

# initiera
# yttre loop
# inre loop
# default message


def save_to_logg(member):
    date_time_now = datetime.datetime.now()
    time_now_str = date_time_now.strftime("%H:%M:%S")
    time_checkedin = member[2]
    global loggSheet
    row = str(loggSheet.max_row + 1)
    loggSheet['A' + row] = member[1] # date
    loggSheet['B' + row] = member[0] # name
    loggSheet['C' + row] = time_checkedin
    loggSheet['D' + row] = time_now_str
    if time_now_str < time_checkedin:
        loggSheet['E' + row] = "Late checkout"

def checkin_member(key, member):
    date_time_now = datetime.datetime.now()
    time_now_str = date_time_now.strftime("%H:%M:%S")
    date_now_str = date_time_now.strftime("%Y-%m-%d")
    if member[1]: 
        checked_in_styret[key] = [member[0], date_now_str, time_now_str]
    else:
        checked_in_members[key] = [member[0], date_now_str, time_now_str]

# Start of main here
message_update_time_short = 2
message_update_time_long = 5
latest_message_time = datetime.datetime.now()

init_member_register()
init_log()
update_lists()
message_variable.set("Please swipe your card")


while True:
    update_lists()
#    mv_incheckade_png()
    while line_count(text.get('1.0',tk.END+"-1c")) < 1:
        timed_functions()
        date_time_now = datetime.datetime.now()
        if (latest_message_time < date_time_now):
            message_variable.set("Please swipe your card")
        root.update()

    card_number = text.get('1.0',tk.END+"-1c")[:-1]
    text.delete('1.0', tk.END)
    
    if card_number in commands:
        func = commands[card_number]
        func()
    else:
        card_number = '0,' + card_number
        # Number was read
        time_now_str = date_time_now.strftime("%H:%M:%S")
        date_now_str = date_time_now.strftime("%Y-%m-%d")

        if card_number in checked_in_members:
            message_variable.set('Goodbye %s' %checked_in_members[card_number][0])
            save_to_logg(checked_in_members[card_number])
            del checked_in_members[card_number]
            update_lists()
            root.update()
            latest_message_time = date_time_now + datetime.timedelta(0,message_update_time_short)
            # spara i loggboken
        elif card_number in checked_in_styret:   
            message_variable.set('Goodbye %s' %checked_in_styret[card_number][0])
            save_to_logg(checked_in_styret[card_number])
            del checked_in_styret[card_number]
            update_lists()
            root.update()
            latest_message_time = date_time_now + datetime.timedelta(0,message_update_time_short)

            # spara i loggboken
        elif card_number in member_register:
            message_variable.set('Welcome %s' %member_register[card_number][0])
            checkin_member(card_number, member_register[card_number])
            update_lists()
            root.update()
            latest_message_time = date_time_now + datetime.timedelta(0,message_update_time_short)
            # då ska vi checka in
        else:
            time_to_wait = 5
            old_card_number = card_number
            time_flag = True
            date_time_to_wait = datetime.datetime.now() + datetime.timedelta(0,time_to_wait)

            while (line_count(text.get('1.0',tk.END+"-1c")) < 1) and (date_time_to_wait > datetime.datetime.now()):
                message_variable.set('Card not recognised!\nPlease scan again to start a transfer process,\nor wait %s seconds to cancel' %second_counter(date_time_to_wait))
                root.update()
            
            if not (line_count(text.get('1.0',tk.END+"-1c")) < 1):
                new_card_number = '0,' + text.get('1.0',tk.END+"-1c")[:-1]
                if new_card_number == old_card_number:
                    date_time_to_wait = datetime.datetime.now() + datetime.timedelta(0,time_to_wait)
                    
                    while (line_count(text.get('1.0',tk.END+"-1c")) < 1) and (date_time_to_wait > datetime.datetime.now()):
                        message_variable.set('Now scan your old card that you want to transfer your data from,\nor wait %s seconds to cancel' %str(time_to_wait))
                        root.update()
                    new_card_number = '0,' + text.get('1.0',tk.END+"-1c")[:-1]
                    if not (line_count(text.get('1.0',tk.END+"-1c")) < 1):
                        text.delete('1.0', tk.END)
                        if old_card_number in member_register:
                            member_register[new_card_number] = member_register[old_card_number]
                            del member_register[old_card_number]
                            save_memberlist_to_file()
                        else:
                            message_variable.set('Old card not in member database...\nTransfer failed.')
                            root.update()
                            latest_message_time = datetime.datetime.now() + datetime.timedelta(0,message_update_time_long)
                    else:
                        message_variable.set("Aborted!")
                        text.delete('1.0', tk.END)
                        root.update()
                        latest_message_time = datetime.datetime.now() + datetime.timedelta(0,message_update_time_short)
                else:
                    message_variable.set("Aborted!")
                    text.delete('1.0', tk.END)
                    root.update()
                    latest_message_time = datetime.datetime.now() + datetime.timedelta(0,message_update_time_short)

            else:
                message_variable.set("Aborted!")
                text.delete('1.0', tk.END)
                root.update()
                latest_message_time = datetime.datetime.now() + datetime.timedelta(0,message_update_time_short)

