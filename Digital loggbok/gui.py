import tkinter as tk
import datetime

class LoggbookGUI(object):
    """docstring for GUI"""
    def __init__(self):

        message_area_bg_color = 'black'
        message_area_fg_color = 'white'
        input_area_bg_color = 'black'
        input_area_fg_color = 'white'
        member_title = "Checked-in members"
        styret_title = "Checked-in board members"
        member_title_offsetX = 5
        member_title_offsetY = 250
        styret_title_offsetX = member_title_offsetX
        styret_title_offsetY = 0
        title_color = "black"
        title_size = 36
        title_font = ('Arial', title_size, 'bold')
        main_window_width = 700
        main_window_height = 800
        x = 10
        y = 10
        self.namelist_color = "black"
        namelist_size = 18
        self.namelist_font=('Arial', namelist_size)
        namelist_row_padding = 5
        namelist_col_padding = 10
        self.styret_namelist_offsetX = namelist_col_padding
        self.styret_namelist_offsetY = styret_title_offsetY + namelist_row_padding + title_size
        self.member_namelist_offsetX = namelist_col_padding
        self.member_namelist_offsetY = member_title_offsetY + namelist_row_padding + title_size
        interactive_area_width = main_window_width
        interactive_area_height = 80
        message_area_height = 65
        input_area_height = 15
        message_height = message_area_height - input_area_height
        message_area_width = main_window_width
        message_width = message_area_width
        input_area_width = message_area_width
        styret_namelist = ""
        member_namelist = ""
        app_title = "XP digital logg v2.0"
        file_name_bg = "bg.gif"

        self.root = tk.Tk()
        self.message_variable = tk.StringVar()
        self.cv = tk.Canvas(bg='white')

        self.root.title(app_title)
        self.root.geometry("%dx%d+%d+%d" % (main_window_width, main_window_height, x, y))
        in_file = open(file_name_bg, "rb")
        data_bytes = in_file.read()
        in_file.close()
        self.photo = tk.PhotoImage(data=data_bytes)
        self.cv.configure(width=665, height=660)
        self.cv.pack(side=tk.TOP, expand=False)
        self.cv.create_image(25, 25, image=self.photo, anchor='nw')
        self.cv.create_text(member_title_offsetX, member_title_offsetY, fill=title_color,
        						 font=title_font, anchor='nw', text=member_title)
        self.cv.create_text(styret_title_offsetX, styret_title_offsetY, fill=title_color,
        						font=title_font, anchor='nw', text=styret_title)
        interactive_area = tk.Frame(self.root, bg=message_area_bg_color, width = interactive_area_width, height = interactive_area_height)
        message_area = tk.Frame(interactive_area, bg=message_area_bg_color, width = message_area_width, height = message_area_height, bd = 0)
        message = tk.Message(message_area, bg=message_area_bg_color, width = 500, fg = message_area_fg_color, textvariable = self.message_variable)
        self.text = tk.Text(interactive_area, height=input_area_height, width=input_area_width, bg=input_area_bg_color, foreground=input_area_fg_color, bd = 0)
        interactive_area.pack(side=tk.BOTTOM, expand=False)
        message_area.pack(side=tk.TOP, expand = False)
        message_area.pack_propagate(False)
        self.message_variable.set("Please swipe your card")
        message.configure(font=('Arial', 18, 'bold'))
        message.pack(side=tk.TOP, expand=False)
        self.text.pack(side=tk.BOTTOM, expand=False)
        self.text.focus()
        self.latest_message_time = datetime.datetime.now()

    def update_lists(self, list_of_memberstring, list_tag):
        self.cv.delete(list_tag)
        next_col = 300
        idx = 0
        if list_tag == 'styret_names':
            namelist_offsetX = self.styret_namelist_offsetX
            namelist_offsetY = self.styret_namelist_offsetY
        else:
            namelist_offsetX = self.member_namelist_offsetX
            namelist_offsetY = self.member_namelist_offsetY
        for items in list_of_memberstring:
            self.cv.create_text(namelist_offsetX + next_col * idx, namelist_offsetY,
                            fill=self.namelist_color, font=self.namelist_font, anchor='nw', text=items, tag=list_tag)
            idx = idx + 1
        self.root.update()

    def message(self, message_string, message_time=0):
        self.message_variable.set(message_string)
        self.latest_message_time = datetime.datetime.now() + datetime.timedelta(0,message_time)
        self.root.update()

    def has_lines(self):
        input_text = self.text.get('1.0',tk.END+"-1c")
        self.root.update()
        return sum(1 for char in input_text if char == '\n')

    def remove_input(self):
        self.text.delete('1.0', tk.END)
    
    def read_input(self):
        txt = self.text.get('1.0',tk.END+"-1c")[:-1]
        self.remove_input()
        return txt
        
