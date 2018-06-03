import tkinter as tk
from datetime import datetime, timedelta

styret_namelist = ""
member_namelist = ""
app_title = "XP digital logg v2.0"
member_title = "Checked-in members"
styret_title = "Checked-in board members"
file_name_bg = "bg.gif"
message_area_bg_color = 'black'
message_area_fg_color = 'white'
input_area_bg_color = 'black'
input_area_fg_color = 'white'
namelist_color = "black"
title_color = "black"
title_size = 36
namelist_size = 18
title_font = ('Arial', title_size, 'bold')
namelist_font=('Arial', namelist_size)

member_title_offsetX = 5
member_title_offsetY = 250
styret_title_offsetX = member_title_offsetX
styret_title_offsetY = 0
main_window_width = 700
main_window_height = 800
x = 10
y = 10
namelist_row_padding = 5
namelist_col_padding = 10
interactive_area_height = 80
message_area_height = 65
input_area_height = 15
styret_namelist_offsetX = namelist_col_padding
styret_namelist_offsetY = styret_title_offsetY + namelist_row_padding + title_size
member_namelist_offsetX = namelist_col_padding
member_namelist_offsetY = member_title_offsetY + namelist_row_padding + title_size
interactive_area_width = main_window_width
message_height = message_area_height - input_area_height
message_area_width = main_window_width
message_width = message_area_width
input_area_width = message_area_width


root = tk.Tk()
message_variable = tk.StringVar()
cv = tk.Canvas(bg='white')

root.title(app_title)
root.geometry("%dx%d+%d+%d" % (main_window_width, main_window_height, x, y))
in_file = open(file_name_bg, "rb")
data_bytes = in_file.read()
in_file.close()
photo = tk.PhotoImage(data=data_bytes)
cv.configure(width=665, height=660)
cv.pack(side=tk.TOP, expand=False)
cv.create_image(25, 25, image=photo, anchor='nw')

cv.create_text(member_title_offsetX, member_title_offsetY, fill=title_color,
               font=title_font, anchor='nw', text=member_title)
cv.create_text(styret_title_offsetX, styret_title_offsetY, fill=title_color,
               font=title_font, anchor='nw', text=styret_title)
interactive_area = tk.Frame(root, bg=message_area_bg_color,width=interactive_area_width,
                            height=interactive_area_height)
message_area = tk.Frame(interactive_area, bg=message_area_bg_color,
                        width=message_area_width, height=message_area_height, bd = 0)
message = tk.Message(message_area, bg=message_area_bg_color, width=500, 
                     fg=message_area_fg_color, textvariable=message_variable)
text = tk.Text(interactive_area, height=input_area_height, width=input_area_width,
               bg=input_area_bg_color, foreground=input_area_fg_color, bd = 0)

interactive_area.pack(side=tk.BOTTOM, expand=False)
message_area.pack(side=tk.TOP, expand = False)
message_area.pack_propagate(False)
message_variable.set("Please swipe your card")
message.configure(font=('Arial', 18, 'bold'))
message.pack(side=tk.TOP, expand=False)
text.pack(side=tk.BOTTOM, expand=False)
text.focus()
latest_message_time = datetime.now()

def update_lists(list_of_memberstring, list_tag):
    cv.delete(list_tag)
    next_col = 300
    idx = 0
    if list_tag == 'styret_names':
        namelist_offsetX = styret_namelist_offsetX
        namelist_offsetY = styret_namelist_offsetY
    else:
        namelist_offsetX = member_namelist_offsetX
        namelist_offsetY = member_namelist_offsetY
    for items in list_of_memberstring:
        cv.create_text(namelist_offsetX + next_col * idx, namelist_offsetY,
                        fill=namelist_color, font=namelist_font, anchor='nw', 
                        text=items, tag=list_tag)
        idx = idx + 1
    root.update()

def message(message_string, message_time=0):
    message_variable.set(message_string)
    global latest_message_time
    latest_message_time = datetime.now() + timedelta(0,message_time)
    root.update()

def has_lines():
    input_text = text.get('1.0',tk.END+"-1c")
    root.update()
    return sum(1 for char in input_text if char == '\n')

def remove_input():
    text.delete('1.0', tk.END)

def read_input():
    txt = text.get('1.0',tk.END+"-1c")[:-1]
    remove_input()
    return txt
    