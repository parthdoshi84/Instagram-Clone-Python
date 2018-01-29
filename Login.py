from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk
from dbConnection import dbConnection
from HomePage import Home_Page
from SignUp import SignUp
from ttk import Frame, Style


class Login:

    def __init__(self,root):
        self.root = root
        self.root.configure(background="#212121")
        width = 320
        height = 680
        self.root.minsize(width=320, height=480)
        self.root.maxsize(width=320, height=480)

        image = Image.open("logo.png")
        image = image.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = Label(self.root, image=img , bg = "#212121")
        panel.image = img
        panel.pack(side = TOP ,padx = (0,0))

        ##insert your image here(icon for your hope)
        image1 = Image.open("Instagram_logo.png")
        image1 = image1.resize((128, 46), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(image1)
        panel1 = Label(self.root, image=img1, bg="#212121")
        panel1.image = img1
        panel1.pack(side=TOP, pady=(0, 50))

        #widgets

        self.username = Label(self.root,text = "Username",bg = "#212121", fg = "#d3d3d3")
        self.password = Label(self.root, text="Password",bg = "#212121",fg = "#d3d3d3")
        self.user_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")
        self.pass_entry = Entry(self.root, bg = "#424242",width = 30 , fg ="#d3d3d3")
        self.login = Button(self.root, text = "Login",command = self.Login_Event,bg = "#178fff",fg = "white",width = 10)
        self.signup = Label(self.root,text = "Sign Up First",bg = "#212121", fg = "#178fff", font = "none 10 underline")
        #self.upload = Button(root, text="Upload", command=self.Signup_Event)

        #position
        self.username.pack(side = TOP ,padx = (0,120), pady = (0,5))
        self.user_entry.pack(side=TOP, padx=(0,0), pady=(0, 10))
        self.password.pack(side = TOP,padx = (0,120), pady = (0,5))
        self.pass_entry.pack(side =TOP,padx = (0,0), pady = (0,20))
        self.login.pack(side = TOP, padx = (10,0),pady=(0, 15))
        self.signup.pack(side=TOP, padx = (10,0))

        self.signup.bind('<Button-1>', self.Signup_Event)


    def Login_Event(self):
        dbconnection = dbConnection()
        self.username_input = self.user_entry.get()
        self.password_input = self.pass_entry.get()
        profile , user , friends, pictures = dbconnection.retrieve(self.username_input, self.password_input)
        self.root.destroy()
        ##make an object of your class here. Don't waste time in making this:)
        root = Tk()
        home_page = Home_Page(root,user ,dbconnection ,friends,pictures,profile)
        root.mainloop()

    def Signup_Event(self,event):
        self.root.destroy()
        root = Tk()
        signup = SignUp(root)
        root.mainloop()
