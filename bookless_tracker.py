import os
import sys
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont

checkboxes = {}
button_commands = {}
button_vars = {}
labels = {}
buildings_count = 1


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = button_vars[pick.lower()] if pick.lower() in button_vars else IntVar()

            def icon_toggle(icon_name=pick.lower()):
                if button_vars[icon_name].get():
                    x, y = icon_positions[icon_name]
                    labels[icon_name].place(x=x, y=y)
                else:
                    labels[icon_name].place_forget()

            def building_toggle(building_name=pick.lower(), building_var=var):
                global buildings_count
                if building_name == "monster hut 3":
                    return
                if building_var.get():
                    buildings_count += 1
                else:
                    buildings_count -= 1
                name_or_count_changed(None)

            chk = Checkbutton(self, text=pick, variable=var, command=icon_toggle if pick.lower() in labels else building_toggle)
            chk.configure(background='#D39B6A', activebackground='#D39B6A')
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


if __name__ == '__main__':
    # Checklist window
    root = Tk()
    root.title('Bookless checklist')
    root.configure(background='#26AFF3')

    row = 0

    def create_checklist(label, entries):
        global row
        label = Label(root, text=label, font=('Helvetica', 10, 'bold'), background='#26AFF3')
        label.grid(row=row, sticky=W, padx=2, pady=0)
        checkbar = Checkbar(root, entries)
        checkbar.grid(row=row+1, sticky=W, padx=2, pady=0)
        checkbar.config(relief=GROOVE, bd=2)
        row += 2

    # Graphic display window
    graphic = Tk()
    graphic.title("Bookless graphical display")
    graphic.geometry("512x160")

    save_screen = Image.open(resource_path("data/save_screen.png"))
    save_photo = ImageTk.PhotoImage(save_screen, master=graphic)
    save_label = Label(graphic, image=save_photo, borderwidth=0)
    save_label.place(x=0, y=0)

    photos = []
    icon_positions = {'nico': (39, 80), 'selfi': (71, 80), 'fur': (103, 80), 'patty': (135, 80), 'vivian': (167, 80), 'mia': (199, 80), 'cherrl': (231, 80), 'beldo':(264, 80), 'blue collar': (374, 38), 'windmills': (406, 38), 'pool': (438, 38)}
    for icon, (x, y) in icon_positions.items():
        image = Image.open(resource_path('data/' + icon + '.png'))
        photo = ImageTk.PhotoImage(image, master=graphic)
        photos.append(photo)  # keep pointers in memory
        label = Label(graphic, image=photo, borderwidth=0)
        label.place(x=x, y=y)
        label.place_forget()
        labels[icon] = label

        icon_var = IntVar()
        button_vars[icon] = icon_var

    # Create checkbuttons linked to images
    create_checklist('Girls', ['Nico', 'Selfi', 'Fur', 'Patty', 'Vivian', 'Mia', 'Cherrl'])
    create_checklist('House upgrades',
                     ['House 1', 'House 2', 'Monster Hut 1', 'Monster Hut 2', 'Monster Hut 3', 'Monster Hut 4'])
    create_checklist('Buildings',
                     ['Racetrack', 'Temple', 'Casino', 'Hospital', 'Fountain', 'Library', 'Theater', 'Bowling Alley',
                      'Arcade', 'Gym'])
    create_checklist('Quests', ['Blue Collar', 'Windmills', 'Pool', 'Beldo'])

    # name field
    name_var = StringVar()
    name_var.set("Koh")
    name_label = Label(root, text='Name', font=('Helvetica', 10, 'bold'), background='#26AFF3')
    name_label.grid(row=row, sticky=W, padx=2, pady=0)
    row += 1
    name_entry = Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))
    name_entry.grid(row=row, sticky=W, padx=4, pady=4)

    def name_or_count_changed(event):
        global save_label, save_photo
        save_screen = Image.open(resource_path("data/save_screen.png"))
        draw = ImageDraw.Draw(save_screen)
        azure_font = ImageFont.truetype(resource_path('data/Azure_Dreams.ttf'), 30)
        draw.text((130, 19), name_var.get()[:15], font=azure_font, fill='black')
        draw.text((464, 83), str(buildings_count), font=azure_font, fill='black')
        save_photo = ImageTk.PhotoImage(save_screen, master=graphic)
        save_label.configure(image=save_photo)
    name_or_count_changed(None)

    root.bind('<Return>', name_or_count_changed)

    # def reset():
    #     for widget in root.winfo_children():
    #         if isinstance(widget, Checkbar):
    #             for w in widget.winfo_children():
    #                 if isinstance(w, Checkbutton):
    #                     w.deselect()
    # Button(root, text='Clear', command=reset).grid(row=row, sticky=E, padx=4, pady=4)

    # run
    root.mainloop()



