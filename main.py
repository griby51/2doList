#2doList
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import json

lists = []

def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

def refreshLists(_lists):
    with open("data.json", "r") as f:
        _lists = json.load(f)["lists"]
    return _lists

window = tk.Tk()
window.title("2doList")
window.resizable(width=False, height=True)
window.geometry("1080x720")
window.minsize(1080, 720)
window.configure(bg="#1e1e1e")

inactiveAddListBtnImg = tk.PhotoImage(file="assets/addListBtnInactive.png") 
inactiveAddListBtnLabel = tk.Label(window, image=inactiveAddListBtnImg, bg="#1e1e1e")

titleLabelList = tk.Label(window, text="Vos listes :", font=("Arial", 20), fg="#00b1b1", bg="#1e1e1e")

#pack at the top lefttitleLabelList.grid(row=1, column=2)

titleLabelList.pack(anchor="nw", padx=20, pady=10)
inactiveAddListBtnLabel.pack()


lists = refreshLists(lists)
for list in lists:
    activeBackgoundSquare = tk.PhotoImage(file="assets/emptyActiveButton.png")
    inactiveBackgoundSquare = tk.PhotoImage(file="assets/emptyInactiveButton.png")

    listIsSelected = ttk.Checkbutton(window, text=strike(list["name"]), image=inactiveBackgoundSquare)
    
    























col_count, row_count = window.grid_size()

for i in range(col_count):
    window.columnconfigure(i, minsize=10)

for i in range(row_count):
    window.rowconfigure(i, minsize=10)
window.mainloop()