from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk
from Profile import Profile

class Home_Page:
    def __init__(self,root,user, dbconnection,friends,pictures,profile_image):

        self.root = root
        self.root.configure(background="#212121")
        width = 320
        height = 680
        self.root.minsize(width=320, height=480)
        self.root.maxsize(width=320, height=480)

        self.canvas = Canvas(self.root, borderwidth=0, background="#212121")
        self.frame = Frame(self.canvas, background="#212121")
        self.vsb = Scrollbar(self.root, orient="vertical", width = 10, background = "black",command=self.canvas.yview)
        self.vsb.lower(self.frame)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.user= user
        self.dbconnection = dbconnection
        self.friends = friends
        self.pictures = pictures
        self.profile_image = profile_image

        self.initGui()
        self.display()

        self.displayFriends()

        self.profile = Button(self.frame, text="Profile", command=self.Profile_Event, bg="#178fff", fg="white", width=10)
        self.profile.pack(side = TOP,padx = (0,60))

    def onFrameConfigure(self, event):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def initGui(self):
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        image = Image.open("menu1.jpg")
        #image = image.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = Label(self.frame, image=img, bg="#212121")
        panel.image = img
        panel.pack(side =TOP,pady = (0,20),padx = (0,70))

    def display(self):
        for picture in self.pictures:
            picture_image, temp = picture.split("+")
            friend , id  = temp.split("_")

            friend_profile_picture = self.dbconnection.getProfileImage(int(id),friend)
            image1 = Image.open(friend_profile_picture)
            image1 = image1.resize((25, 25), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(image1)
            panel1 = Label(self.frame, image=img1, bg="#212121")
            panel1.image = img1
            panel1.pack(side=TOP,padx = (0,330) )

            label = Label(self.frame, text=friend, bg="#212121", fg="#d3d3d3")
            label.pack(side = TOP, padx = (0,330),pady=(0, 10))

            image = Image.open(picture_image)
            width ,height = image.size
            new_width = 300
            new_height = int(width * height/new_width)
            if new_height>250:
                new_height = 250
            image = image.resize((new_width,new_height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            panel = Label(self.frame, image=img, bg="#212121")
            panel.image = img
            panel.pack(side = TOP , pady = (0,10),padx = (0,90))

            image = Image.open("line.png")
            # image = image.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            panel = Label(self.frame, image=img, bg="#212121")
            panel.image = img
            panel.pack(side=TOP, pady=(0, 10), padx=(0, 70))


    def Profile_Event(self):
        self.root.destroy()
        root = Tk()
        profile = Profile(root,self.dbconnection,self.user,self.friends,self.pictures,self.profile_image)
        root.mainloop()

    def displayFriends(self):
        for friend in self.friends:
            label2 = Label(self.frame, text="Friend", bg="#212121", fg="#178fff")
            label2.pack(side=TOP, padx=(0, 70), pady=(0, 10))
            friend_name, friend_id = friend.split("_")
            friend_id = int(friend_id)
            friend_profile = self.dbconnection.getProfileImage(friend_id, friend_name)
            image1 = Image.open(friend_profile)
            image1 = image1.resize((100, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(image1)
            panel1 = Label(self.frame, image=img1, bg="#212121")
            panel1.image = img1
            panel1.pack(side=TOP, pady=(0, 5), padx=(0, 70))

            label = Label(self.frame, text=friend_name, bg="#212121", fg="#178fff")
            label.pack(side=TOP, padx=(0, 70), pady=(0, 5))



            image = Image.open("line.png")
            # image = image.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            panel = Label(self.frame, image=img, bg="#212121")
            panel.image = img
            panel.pack(side=TOP, pady=(0, 10), padx=(0, 65))
