import tkinter as tk
from tkinter import messagebox as msgbx
from tkinter import filedialog
import json
import numpy as np
import re
import time
import os

from robot import robot
from compiler import Compiler



class interface:
    def __init__(self):
        self.str_res = json.load(open(os.path.join("string_res", "cz.json"), "r", encoding="utf-8"))
        self.main = tk.Tk()
        self.main.title(self.str_res["window_title"])
        self.main.iconbitmap(os.path.join("img","karel.ico"))
        menubar = tk.Menu(self.main)
        menubar.add_command(label=self.str_res["menu_choose_level"], command=self.choose_level)
        self.main.config(menu=menubar)
        self.edit_code = tk.Text(self.main, width=50)
        self.canvas = tk.Canvas(self.main, background = "white")
        self.canvas.grid(row = 0, column = 3, rowspan=2)
        self.karel = robot(self)
   #     self.choose_level()
        self.load(os.path.abspath("levels/basic.map"))
        self.edit_code.grid(row=0, column=0, columnspan=3)
        self.edit_code.insert("end", self.str_res["edit_code_messagge"])
        self.run_button = tk.Button(self.main, text=self.str_res["run_button_label"], command=self.run)
        self.run_button.grid(row=1, column=1, sticky="we")
        self.comp = Compiler(self.karel, self.main)
        self.reset_button = tk.Button(self.main, text=self.str_res["reset_button_label"], command=self.karel.reset_place)
        self.reset_button.grid(row=1, column=0, sticky="we")
        self.stop_button = tk.Button(self.main, text=self.str_res["stop_button_label"], command=self.comp.stop)
        self.stop_button.grid(row=1, column=2, sticky="we")


    def load(self, filename):
        level = json.load(open(filename, "r"))
        self.map = np.array(level["map"])
        height, width = self.map.shape
        self.canvas.config(width = width*50, height = height*50)
        self.canvas.delete("all")
        for y in range(height):
            for x in range(width):
                if self.map[y,x] == 1:
                    self.canvas.create_rectangle(x*50,y*50,(x+1)*50,(y+1)*50, fill="black")
                if self.map[y,x] == 2:
                    self.canvas.create_rectangle(x*50,y*50,(x+1)*50,(y+1)*50, fill="green")
        self.karel.reset_place(level["start"])

    def run(self):
        print("button pressed")
        code = self.edit_code.get(1.0,"end")
        self.comp.run(code)

    def choose_level(self):
        file_name = tk.filedialog.askopenfilename(initialdir=os.path.abspath("/levels/"), title="Choose level", filetypes=(("labyrynths", "*.map"),))
        self.load(file_name)

    def control(self, pos):
        if self.map[pos[1],pos[0]] == 1:
            print("Can't go there. Wall is there.")
            self.comp.stop()
            msgbx.showwarning(title=self.str_res["wall_crash_title"], message=self.str_res["wall_crash_messagge"])
            return(False)
        if self.map[pos[1],pos[0]] == 2:
            self.karel.show()
            self.comp.stop()
            msgbx.showinfo(title=self.str_res["win_title"], message=self.str_res["win_messagge"])
        else: 
            return(True)
    



i = interface()
tk.mainloop()