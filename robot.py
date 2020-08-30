import numpy as np
import tkinter as tk
import os

class robot:
    orientations = [np.array([0,1]), np.array([1,0]), np.array([0,-1]), np.array([-1,0])] #down, right, up, left
    def __init__(self, interface):
        self.pictures = [tk.PhotoImage(file=os.path.join("img/", "robot_0.ppm")),
                         tk.PhotoImage(file=os.path.join("img/", "robot_1.ppm")),
                         tk.PhotoImage(file=os.path.join("img/", "robot_2.ppm")),
                         tk.PhotoImage(file=os.path.join("img/", "robot_3.ppm"))]
        self.canvas = interface.canvas
        self.interface = interface

    def show(self):
        try:
            self.canvas.delete(self.picture)
        except:
            print("no picture to delete")
        self.picture = self.canvas.create_image(50*self.pos[0], 50*self.pos[1],
                                                image = self.pictures[self.orient],
                                                anchor = "nw")
    def left(self):
        if self.orient < 3:
            self.orient += 1
        elif self.orient == 3:
            self.orient = 0
        else:
            print("this should never happen")
        self.show()

    def reset_place(self, start_pos=None):
        if start_pos:
            self.start = start_pos
        self.pos = np.array(self.start)
        self.orient = 1
        self.show()

    def move(self):
        self.pos+=self.orientations[self.orient]
        print(self.pos)
        if self.interface.control(self.pos):
            self.show()
        else: self.reset_place()
