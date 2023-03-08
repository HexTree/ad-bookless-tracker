import os
import sys
from tkinter import *
from PIL import ImageTk, Image

monster_vars = {}
monster_coords = {}


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # Checklist window
    root = Tk()
    root.title('Monster book checklist')
    root.configure(background='#D39B6A')

    # Graphic display window
    graphic = Tk()
    graphic.title("Monster book graphical display")
    graphic.geometry("1141x864")
    save_photo = None
    save_label = Label(graphic, image='', borderwidth=0)
    save_label.place(x=0, y=0)

    book_page_1_col_1 = ['kewne', 'dragon', 'kid', 'ifrit', 'flame', 'grineut', 'griffon', 'troll']
    book_page_1_col_2 = ['balloon', 'volcano', 'barong', 'weadog', 'naplass', 'killer', 'tyrant', 'maximum']
    book_page_2_col_1 = ['saber', 'snowman', 'ashra', 'arachne', 'battnel', 'nyuel', 'pulunpa', 'u-boat']
    book_page_2_col_2 = ['blume', 'manoeva', 'kraken', 'viper', 'mandara', 'glacier', 'takopoo', 'mushrom']
    book_page_3_col_1 = ['death', 'clown', 'univern', 'unicorn', 'metal', 'block', 'noise', 'dreamin']
    book_page_3_col_2 = ['cyclone', 'picket', 'stealth', 'zu', 'garuda', 'golem', 'maliling', 'soilclaw']
    book_page_4 = ['hikewne', 'lazyfrog']

    for i, m in enumerate(book_page_1_col_1):
        monster_coords[m] = (0, 0, i)
    for i, m in enumerate(book_page_1_col_2):
        monster_coords[m] = (0, 1, i)
    for i, m in enumerate(book_page_2_col_1):
        monster_coords[m] = (1, 0, i)
    for i, m in enumerate(book_page_2_col_2):
        monster_coords[m] = (1, 1, i)
    for i, m in enumerate(book_page_3_col_1):
        monster_coords[m] = (2, 0, i)
    for i, m in enumerate(book_page_3_col_2):
        monster_coords[m] = (2, 1, i)
    monster_coords[book_page_4[0]] = (3, 0, 0)
    monster_coords[book_page_4[1]] = (3, 1, 0)
    coords_to_monter = {v: k for k, v in monster_coords.items()}

    monsters = book_page_1_col_1 + book_page_1_col_2 + book_page_2_col_1 + book_page_2_col_2 + book_page_3_col_1 + book_page_3_col_2 + book_page_4
    monsters.sort()

    def update():
        global save_label, save_photo
        save_screen = Image.open(resource_path("data_book/monster_book.png"))

        for monster, var in monster_vars.items():
            if var.get():
                monster_image = Image.open(resource_path('data_book/' + monster + '.png'))
                x, y = 75, 76
                page, col, row = monster_coords[monster]
                if col:
                    x += 256
                y += (36*row)
                if page in (1, 3):
                    x += 576
                if page in (2, 3):
                    y += 432

                save_screen.paste(monster_image, box=(x, y))

        save_photo = ImageTk.PhotoImage(save_screen, master=graphic)
        save_label.configure(image=save_photo)
    update()

    row = 0
    for monster in monsters:
        monster_vars[monster] = IntVar()
        chk = Checkbutton(root, text=monster, variable=monster_vars[monster], command=update)
        chk.configure(background='#D39B6A', activebackground='#D39B6A', padx=12)
        chk.grid(row=row % 25, column=row // 25, sticky=W)
        row += 1

    def handle_mouse_click(event):
        x, y = event.x, event.y
        # find page
        if x >= 576:
            if y >= 432:
                page = 3
            else:
                page = 1
        elif y >= 432:
            page = 2
        else:
            page = 0
        x %= 576
        y %= 432

        # find col
        x -= 25
        col = 1 if x >= 256 else 0

        # find row
        y -= 76
        row = y // 36

        if (page, col, row) in coords_to_monter:
            monster = coords_to_monter[(page, col, row)]
            monster_vars[monster].set(not monster_vars[monster].get())
            update()
    graphic.bind('<Button-1>', handle_mouse_click)

    # run
    root.mainloop()
