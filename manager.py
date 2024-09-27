import os
import shutil
import tkinter as tk
from tkinter import Checkbutton, Frame, IntVar, Scrollbar, Canvas, Button
import zipfile
import imghdr
from PIL import Image

ACTIVE_DIR = 'C:/Users/vanja/AppData/Local/BeamNG.drive/0.33/mods'
INACTIVE_DIR = 'C:/Users/vanja/AppData/Local/BeamNG.drive/disabledMods'
imgs = ['png', 'jpg', 'jpeg']

#show preview
def imgshow(zip_name, active):
    if active:
        imgzip = zipfile.ZipFile(ACTIVE_DIR + "/" + zip_name)
    else:
        imgzip = zipfile.ZipFile(INACTIVE_DIR + "/" + zip_name)
    inflist = imgzip.infolist()

    for f in inflist:
        ifile = imgzip.open(f)
        if (imghdr.what(ifile) in imgs and ('default' in f.filename or 'Default' in f.filename)):
            img = Image.open(ifile)
            print(img, f.filename)
            img.show()

#move archive
def move_archive(zip_name, active):
    if active:
        dest_path = os.path.join(ACTIVE_DIR, zip_name)
        src_path = os.path.join(INACTIVE_DIR, zip_name)
        print(f"Moving {zip_name} to {ACTIVE_DIR}")
    else:
        dest_path = os.path.join(INACTIVE_DIR, zip_name)
        src_path = os.path.join(ACTIVE_DIR, zip_name)
        print(f"Moving {zip_name} to {INACTIVE_DIR}")

    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)
    else:
        print(f"File {zip_name} not found!")

#checkbox check/uncheck handle
def on_check(zip_name, var, root):
    active = var.get()
    move_archive(zip_name, active)
    update_title(root)

#update title counter
def update_title(root):
    active_count = sum(var.get() for var in all_vars)
    root.title(f"Beamng mod manager (Active: {active_count})")

#toggle all checks
def toggle_all(state, root):
    for var in all_vars:
        var.set(state)
    for i, zip_file in enumerate(zip_files):
        move_archive(zip_file, state)
    update_title(root)

#main
def create_app():
    root = tk.Tk()

    canvas = Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(root, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    active_files = [f for f in os.listdir(ACTIVE_DIR) if f.endswith('.zip')]
    inactive_files = [f for f in os.listdir(INACTIVE_DIR) if f.endswith('.zip')]

    global all_vars
    all_vars = []

    global zip_files
    zip_files = []

    def create_zip_row(zip_file, is_active):
        var = IntVar(value=is_active)
        all_vars.append(var)
        zip_files.append(zip_file)

        zip_frame = Frame(scrollable_frame)
        zip_frame.pack(fill=tk.X, padx=5, pady=2)

        checkbutton = Checkbutton(zip_frame, text=zip_file, variable=var,
                                  command=lambda zf=zip_file, v=var: on_check(zf, v, root))
        checkbutton.pack(side=tk.LEFT)

        button = Button(zip_frame, text="preview", command=lambda zf=zip_file: imgshow(zf, var.get()))
        button.pack(side=tk.RIGHT)

    for zip_file in active_files:
        create_zip_row(zip_file, is_active=1)

    for zip_file in inactive_files:
        create_zip_row(zip_file, is_active=0)

    update_title(root)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    toggle_on_button = Button(root, text="enable all", command=lambda: toggle_all(1, root))
    toggle_on_button.pack(side=tk.BOTTOM, pady=10)

    toggle_off_button = Button(root, text="disable all", command=lambda: toggle_all(0, root))
    toggle_off_button.pack(side=tk.BOTTOM, pady=5)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    root.mainloop()

if __name__ == "__main__":
    create_app()

