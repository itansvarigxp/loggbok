import tkinter as tk
#from PIL import Image, ImageTk
from datetime import datetime, timedelta
import paths

# Variabler för namn, font, storlek och så vidare i vyn
styret_namelist = ""
member_namelist = ""
app_title = "XP digital logg v2.0"
member_title = "Checked-in members"
styret_title = "Checked-in board members"
message_area_bg_color = 'black'
message_area_fg_color = 'white'
input_area_bg_color = 'black'
input_area_fg_color = 'white'
namelist_color = "black"
title_color = "black"
title_size = 28
namelist_size = 14
title_font = ('Arial', title_size, 'bold')
namelist_font=('Arial', namelist_size)
permanent_message_font = ('Arial', 22, 'bold') 

# Variabler för offset de olika objekten i vyn
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
interactive_area_height = 40
message_area_height = 65
input_area_height = 15
styret_namelist_offsetX = namelist_col_padding
styret_namelist_offsetY = styret_title_offsetY + namelist_row_padding + title_size
member_namelist_offsetX = namelist_col_padding
member_namelist_offsetY = member_title_offsetY + namelist_row_padding + title_size
interactive_area_width = main_window_width
message_height = message_area_height - input_area_height
message_area_width = main_window_width//2
message_width = message_area_width
input_area_width = message_area_width

# Mögen nedanför skapar layouten till programet
root = tk.Tk()
message_variable = tk.StringVar()
cv = tk.Canvas(bg='white', highlightthickness=0)

root.title(app_title)
root.geometry("%dx%d+%d+%d" % (main_window_width, main_window_height, x, y))
root.configure(background='white')
in_file = open(paths.gui_bg, "rb")
data_bytes = in_file.read()
in_file.close()
photo = tk.PhotoImage(data=data_bytes)

if paths._debug:
	cv.configure(width=665, height=600)
else:
	cv.configure(width=665, height=660)
cv.pack(side=tk.TOP, expand=True)
cv.create_image(25, 25, image=photo, anchor='nw')

cv.create_text(member_title_offsetX, member_title_offsetY, fill=title_color,
               font=title_font, anchor='nw', text=member_title)
cv.create_text(styret_title_offsetX, styret_title_offsetY, fill=title_color,
               font=title_font, anchor='nw', text=styret_title)
interactive_area = tk.Frame(root, bg=message_area_bg_color,width=interactive_area_width,
                            height=interactive_area_height)
message_area = tk.Frame(cv, bg=message_area_bg_color,
                        width=message_area_width, height=message_area_height, bd = 0)
message = tk.Message(message_area, bg=message_area_bg_color, width=500, 
                     fg=message_area_fg_color, textvariable=message_variable)
text = tk.Text(interactive_area, height=input_area_height, width=input_area_width, font=permanent_message_font,
               bg=input_area_bg_color, foreground=input_area_fg_color, bd = 0)

text.tag_configure("center", justify='center')
text.insert(tk.INSERT, "Please scan your card\n")
text.tag_add("center", "1.0", "end")


interactive_area.pack(side=tk.BOTTOM, expand=False)
#message_area.pack(side=tk.TOP, expand = False)
message_area.pack_propagate(False)
#message_variable.set("Please swipe your card")
message.configure(font=('Arial', 14, 'bold'))
#message.pack(side=tk.TOP, expand=False)
message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
text.pack(side=tk.BOTTOM, expand=False)
text.focus()
latest_message_time = datetime.now()

def hideMessage():
    message_area.place_forget()

def showMessage():
    message_area.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# image = Image.open('image.gif')
# copy_of_image = image.copy()
# photo = ImageTk.PhotoImage(image)
# label = ttk.Label(root, image = photo)
# label.bind('<Configure>', resize_image)
# label.pack(fill=BOTH, expand = YES)

# def resize_image(event):
#     new_width = event.width
#     new_height = event.height
#     image = copy_of_image.resize((new_width, new_height))
#     photo = ImageTk.PhotoImage(image)
#     label.config(image = photo)
#     label.image = photo #avoid garbage collection




# Uppdaterar de två olika områden där namn skrivs ut, antingen 
# de med styret eller de med medlemmar

member_namelist_rows = 14
styret_namelist_rows = 10
namelist_colspacing = 300
namelist_rowspacing = 20

def updateNames(list_of_members, list_tag):
    cv.delete(list_tag)
    item_nbr = 0

    if list_tag == 'styret':
        namelist_offsetX = styret_namelist_offsetX
        namelist_offsetY = styret_namelist_offsetY
        items_per_row = styret_namelist_rows
    else:
        namelist_offsetX = member_namelist_offsetX
        namelist_offsetY = member_namelist_offsetY
        items_per_row = member_namelist_rows
    
    for member in list_of_members:
        name = list_of_members[member].getName()
        cv.create_text(namelist_offsetX + (item_nbr // items_per_row) * namelist_colspacing,
                       namelist_offsetY + (item_nbr % items_per_row) * namelist_rowspacing,
                        fill=namelist_color, font=namelist_font, anchor='nw', 
                        text=name, tag=list_tag)
        item_nbr += 1
    root.update()


def message(message_string, message_time=0):
    global latest_message_time
    latest_message_time = datetime.now() + timedelta(0,message_time)
    if message_string == message_variable.get():
        return
    else:
        showMessage()
        message_variable.set(message_string)

# Kollar om det finns en ny rad i input-text rutan
def hasLines():
    input_text = text.get('2.0',tk.END+"-1c")
    root.update()
    return sum(1 for char in input_text if char == '\n')

# Tar bort alla rader i input text rutan
def removeInput():
    text.delete('2.0', tk.END+"-1c")

# Returnerar det som står i textrutan och renar den
def readInput():
    txt = text.get('2.0',tk.END+"-1c")[:-1]
    removeInput()
    return txt
    
