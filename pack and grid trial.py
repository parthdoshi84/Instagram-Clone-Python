from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk
from dbConnection import dbConnection
from circularImages import circular_image
import time

class Profile:
    def __init__(self,root):
        self.root = root
        self.root.configure(background="#212121")
        width = 320
        height = 680
        self.root.minsize(width=320, height=480)
        self.root.maxsize(width=320, height=480)

        self.canvas = Canvas(self.root, borderwidth=0, background="#212121")
        self.frame = Frame(self.canvas, background="#212121")
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(background="#212121",yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        label1 = Label(self.frame, text = "Frame1")
        label1.pack(side = TOP , fill = X )

        label2 = Label(self.frame, text = "Frame2")
        label2.grid(row = 1 ,column = 0)

        label3 = Label(self.frame, text="Frame3")
        label3.grid(row = 1 ,column = 1)

        label4 = Label(self.frame, text="Frame4")
        label4.grid(row = 1 ,column =2)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

root = Tk()
profile = Profile(root)
root.mainloop()

