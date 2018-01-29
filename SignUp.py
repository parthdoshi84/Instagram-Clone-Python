from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk
from dbConnection import dbConnection
from Profile import Profile

class SignUp:
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
        panel = Label(self.root, image=img, bg="#212121")
        panel.image = img
        panel.pack(side=TOP, padx=(0, 0))

        image1 = Image.open("Instagram_logo.png")
        image1 = image1.resize((128, 46), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(image1)
        panel1 = Label(self.root, image=img1, bg="#212121")
        panel1.image = img1
        panel1.pack(side=TOP, pady=(0, 5))

        #widgets
        self.name = Label(self.root,text = "Name" , bg = "#212121", fg = "#d3d3d3")
        self.username = Label(self.root,text = "Username",bg = "#212121", fg = "#d3d3d3")
        self.password = Label(self.root, text="Password",bg = "#212121", fg = "#d3d3d3")
        self.country = Label(self.root, text="Country",bg = "#212121", fg = "#d3d3d3")
        self.mobile = Label(self.root, text="Mobile",bg = "#212121", fg = "#d3d3d3")
        self.name_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")
        self.user_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")
        self.pass_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")
        self.country_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")
        self.mobile_entry = Entry(self.root, bg = "#424242",width = 30 , fg = "#d3d3d3")

        self.signup = Button(root, text = "Signup", command = self.Signup_Event,bg = "#178fff",fg = "white",width = 10)


        #position
        self.name.pack(side=TOP, padx=(0, 140), pady=(0, 5))
        self.name_entry.pack(side=TOP, padx=(0, 0), pady=(0, 10))
        self.username.pack(side=TOP, padx=(0, 140), pady=(0, 5))
        self.user_entry.pack(side=TOP, padx=(0, 0), pady=(0, 10))
        self.password.pack(side=TOP, padx=(0, 140), pady=(0, 5))
        self.pass_entry.pack(side=TOP, padx=(0, 0), pady=(0, 20))
        self.country.pack(side=TOP, padx=(0, 140), pady=(0, 5))
        self.country_entry.pack(side=TOP, padx=(0, 0), pady=(0, 10))
        self.mobile.pack(side=TOP, padx=(0, 140), pady=(0, 5))
        self.mobile_entry.pack(side=TOP, padx=(0, 0), pady=(0, 15))

        self.signup.pack(side=TOP, padx=(10, 0))

        #self.signup.bind('<Signup>',self.signup)

    def Signup_Event(self):
        dbconnection = dbConnection()
        self.name_input = self.name_entry.get()
        self.username_input = self.user_entry.get()
        self.password_input = self.pass_entry.get()
        self.country_input = self.country_entry.get()
        self.mobile_input = self.mobile_entry.get()

        dbconnection.insert(self.name_input,self.username_input,self.password_input,self.country_input,self.mobile_input)
        profile_image, user, friends, pictures = dbconnection.retrieve(self.username_input, self.password_input)

        self.root.destroy()
        root = Tk()
        profile = Profile(root,dbconnection,user,friends,pictures,profile_image)
        root.mainloop()