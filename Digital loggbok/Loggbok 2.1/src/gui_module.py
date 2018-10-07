import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from datetime import datetime, timedelta
from member import Member
from excel_handler import styret_titles
from os import listdir
from os.path import isfile, join, basename, splitext
import random
import paths

# Variabler för namn, font, storlek och så vidare i vyn
styret_namelist = ""
member_namelist = ""
app_title = "XP digital logg v3.0"
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
member_title_offsetY = 200
styret_title_offsetX = member_title_offsetX
styret_title_offsetY = 0
main_window_width = 700
main_window_height = 800
x = 10
y = 10
namelist_row_padding = 5
namelist_col_padding = 10
interactive_area_height = 70

message_area_height = 100
message_area_width = 600

input_area_height = 15

namelist_colspacing = 250
namelist_rowspacing = 20

styret_namelist_offsetX = namelist_col_padding
styret_namelist_offsetY = styret_title_offsetY + namelist_row_padding + title_size
member_namelist_offsetX = namelist_col_padding
member_namelist_offsetY = member_title_offsetY + namelist_row_padding + title_size
interactive_area_width = main_window_width
message_height = message_area_height - input_area_height
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

cv.board_members = {}

def resize_image(event):
    new_size = min(event.width, event.height)
    global member_namelist_offsetY
    member_namelist_offsetY = max(0,event.height-member_title_offsetY) + namelist_row_padding + title_size
    image = copy_of_image.resize((new_size-50, new_size-50))
    photo = ImageTk.PhotoImage(image)
    cv.delete("all")
    cv.create_image(event.width/2, event.height/2, image=photo, anchor='center', tag='background')
    cv.create_text(member_title_offsetX, max(0,event.height-member_title_offsetY), fill=title_color,
               font=title_font, anchor='nw', text=member_title)
    cv.create_text(styret_title_offsetX, styret_title_offsetY, fill=title_color,
               font=title_font, anchor='nw', text=styret_title)
    updateNames(Member.checked_in_members, 'member')
    updateNames(Member.checked_in_styret, 'styret')
    cv.image = photo #avoid garbage collection
    cv.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

def replace_areas(event):
    cv.configure(width=root.winfo_width(), height=root.winfo_height()-interactive_area_height)

image = Image.open(paths.gui_bg)
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
#cv = ttk.Label(root, image = photo)
root.bind('<Configure>', replace_areas)
cv.bind('<Configure>', resize_image)
cv.create_image(25, 25, image=photo, anchor='nw', tag='background')
cv.pack(side=tk.TOP, expand=True)


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

# Uppdaterar de två olika områden där namn skrivs ut, antingen 
# de med styret eller de med medlemmar
#source_tmp = Image.open(paths.board_members_local_path + "default.png")
image_size_ratio = 2/3

minimum_imageY = 100
maximum_imageY = 300
default_imageY = maximum_imageY
minimum_image_size = (int(image_size_ratio*minimum_imageY), minimum_imageY)
maximum_image_size = (int(image_size_ratio*maximum_imageY), maximum_imageY)
styret_image_padY = 10
styret_text_padX = 10
image_size = (int(image_size_ratio*default_imageY), default_imageY)
#image = ImageOps.fit(source_tmp, image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
#cv.default_boardmember = ImageTk.PhotoImage(image)
cv.boardmember_img_src = {}
cv.boardmember_img_fit = {}
cv.default_boardmember_img_src = {}
cv.default_boardmember_img_fit = {}

def loadDefaultImagesSource():
    onlyfiles = [f for f in listdir(paths.board_members_local_path) if isfile(join(paths.board_members_local_path, f))]
    i = 1
    if len(onlyfiles) == 0:
        in_file = Image.open(paths.res_path + "default.jpg")
        tmp = ImageOps.fit(in_file, maximum_image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
        cv.default_boardmember_img_src[i] = tmp
    else:
        for file in onlyfiles:
            if file[:7] == "default":
                try:
                    in_file = Image.open(paths.board_members_local_path + file)
                    tmp = ImageOps.fit(in_file, maximum_image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
                    cv.default_boardmember_img_src[i] = tmp
                    i += 1
                except:
                    pass



def getBoardmembersImagesExtern():
    onlyfiles = [f for f in listdir(paths.board_members_extern_path) if isfile(join(paths.board_members_extern_path, f))]
    for file in onlyfiles:
        try:
            in_file = Image.open(paths.board_members_extern_path + file)
            tmp = ImageOps.fit(in_file, maximum_image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
            tmp.save(paths.board_members_local_path + file)
        except:
            pass


def loadBoardmembersImagesSource():
    onlyfiles = [f for f in listdir(paths.board_members_local_path) if isfile(join(paths.board_members_local_path, f))]
    for file in onlyfiles:
        try:
            in_file = Image.open(paths.board_members_local_path + file)
            tmp = ImageOps.fit(in_file, maximum_image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5))
            if file[:7] != "default":
                cv.boardmember_img_src[basename(splitext(file)[0])] = tmp
        except:
            pass

getBoardmembersImagesExtern()
loadDefaultImagesSource()
loadBoardmembersImagesSource()
size_table = {}

def updateImageSize(items_to_be_placed):
    global image_size
    current_image_size = image_size
    area_width = int(root.winfo_width())
    area_height = member_namelist_offsetY - styret_namelist_offsetY
    key = (area_width, area_height, items_to_be_placed)
    items_per_col = area_height // (image_size[1] + 2*styret_image_padY)
    items_per_row = (area_width // (namelist_colspacing + image_size[0] ))
    maximum_nbr_items = items_per_col * items_per_row
    if not key in size_table:
        if items_to_be_placed > maximum_nbr_items:
            newY_rows = area_height / (items_per_col + 1 ) - 2*styret_image_padY
            newY_cols = (area_width / (items_per_row + 1 ) - namelist_colspacing) / image_size_ratio
            newY = max(max(newY_rows, newY_cols), minimum_imageY)
            size_table[key] = (int(image_size_ratio*newY), int(newY))
            image_size = size_table[key]
        else:
            size_table[key] = image_size
    else:
        image_size = size_table[key]


def updateNames(list_of_members, list_tag):
    cv.delete(list_tag)
    item_nbr = 0
    global image_size
    if list_tag == 'styret':

        updateImageSize(len(list_of_members))
        namelist_offsetX = styret_namelist_offsetX
        namelist_offsetY = styret_namelist_offsetY
        i = 0

        for member in list_of_members:
            board_member = list_of_members[member]
            name = board_member.getName()
            if name in styret_titles:
                title = styret_titles[name]
            else:
                title = ""
            if name in cv.boardmember_img_src:
                picture = ImageTk.PhotoImage(ImageOps.fit(cv.boardmember_img_src[name], image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5)))
                cv.boardmember_img_fit[i] = picture
                i += 1
            else:
                idx = random.randint(1,len(cv.default_boardmember_img_src))
                picture = ImageTk.PhotoImage(ImageOps.fit(cv.default_boardmember_img_src[idx], image_size, method=Image.ANTIALIAS, bleed=0.0, centering=(0.5, 0.5)))
                cv.boardmember_img_fit[i] = picture
                i += 1

            items_per_row = (member_namelist_offsetY - styret_namelist_offsetY) // (image_size[1] + 2*styret_image_padY)
            
            cv.create_image((item_nbr // items_per_row) * (namelist_colspacing + image_size[0]), 
                            namelist_offsetY + (item_nbr % items_per_row) * (image_size[1] + styret_image_padY), 
                            image=picture, anchor='nw', tag=list_tag)
            cv.create_text(styret_text_padX + image_size[0] + (item_nbr // items_per_row ) * (namelist_colspacing + image_size[0]),
                           namelist_offsetY + ((item_nbr % items_per_row)) * image_size[1] + image_size[1]/2,
                           fill=namelist_color, font=namelist_font, anchor='w', 
                           text=name.replace(' ', '\n') + "\n"+title, tag=list_tag)
            item_nbr += 1
    else:
        namelist_offsetX = member_namelist_offsetX
        namelist_offsetY = member_namelist_offsetY
        items_per_row = (cv.winfo_height() - member_namelist_offsetY ) // namelist_rowspacing
    
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
    
