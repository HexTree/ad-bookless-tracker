import os
import sys
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont

icon_vars = {}
buildings_vars = {}
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
        for pick in picks:
            pick_name = pick.lower()
            if pick_name in icon_vars:
                var = icon_vars[pick_name]
            else:
                var = IntVar()
                if pick.lower() != "monster hut 3":
                    buildings_vars[pick_name] = var

            chk = Checkbutton(self, text=pick, variable=var, command=update_display)
            chk.configure(background='#D39B6A', activebackground='#D39B6A')
            chk.pack(side=side, anchor=anchor, expand=YES)


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
        icon_vars[icon] = icon_var

    def update_display(event=None):
        global save_label, save_photo, buildings_count
        # update buildings count
        buildings_count = 1
        for var in buildings_vars.values():
            buildings_count += var.get()

        # create updated image with new name and building count
        save_screen = Image.open(resource_path("data/save_screen.png"))
        draw = ImageDraw.Draw(save_screen)
        azure_font = ImageFont.truetype(resource_path('data/Azure_Dreams.ttf'), 30)
        draw.text((130, 19), name_var.get()[:15], font=azure_font, fill='black')
        draw.text((464, 83), str(buildings_count), font=azure_font, fill='black')
        save_photo = ImageTk.PhotoImage(save_screen, master=graphic)
        save_label.configure(image=save_photo)

        # enable/disable icon labels
        for icon, var in icon_vars.items():
            label = labels[icon]
            if var.get():
                label.place(x=icon_positions[icon][0], y=icon_positions[icon][1])
            else:
                label.place_forget()

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

    update_display()
    root.bind('<Return>', update_display)

    def clear():
        for widget in root.winfo_children():
            if isinstance(widget, Checkbar):
                for w in widget.winfo_children():
                    if isinstance(w, Checkbutton):
                        w.deselect()
        update_display()
    Button(root, text='Clear', command=clear).grid(row=row, sticky=E, padx=4, pady=4)

    # run
    root.mainloop()
