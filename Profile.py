from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk
from dbConnection import dbConnection
from circularImages import circular_image
import time
#from HomePage import Home_Page

class Profile:
    def __init__(self,root,dbconnection , user, friends,pictures,profile_image):
        self.root = root
        self.root.configure(background="#212121")
        width = 320
        height = 680
        self.root.minsize(width=320, height=480)
        self.root.maxsize(width=320, height=480)

        self.canvas = Canvas(self.root, borderwidth=0, background="#212121")
        self.frame = Frame(self.canvas, background="#212121")
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.vsb.lower(self.frame)
        self.canvas.configure(background="#212121",yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.dbconnection = dbconnection
        self.user = user
        self.friends  = friends
        self.profile_image = profile_image
        self.pictures = pictures

        self.initGui()

        self.display()

        image = Image.open("line.png")
        # image = image.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = Label(self.frame, image=img, bg="#212121")
        panel.image = img
        panel.pack(side=TOP, pady=(0, 20), padx=(0, 65))


        #self.friend_request = Button(self.frame, text="Send Friend Request", command=self.Send_Request_Event, bg="#178fff", fg="white",
        #                      width=20)
        #self.friend_request.pack(side=TOP, padx=(0, 20),pady =(0,10))

        self.Request_Event()

        self.View_Request_Event()

        self.upload = Button(self.frame, text="Upload", command=self.Upload_Event, bg="#178fff", fg="white",
                             width=10)
        self.upload.pack(side=TOP, padx=(0, 60), pady=(10, 10))

        #self.upload = Button(self.frame, text="Home", command=self.redirect, bg="#178fff", fg="white",
                             #width=10)
        self.upload.pack(side=TOP, padx=(0, 60), pady=(10, 10))
        #self.view_friend_request = Button(self.frame, text="View Friend Request", command=self.View_Request_Event,
                             #       bg="#178fff", fg="white",
                              #      width=20)
        #self.view_friend_request.pack(side=TOP, padx=(0, 20))


    def initGui(self):
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        image = Image.open("menu1.jpg")
        # image = image.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = Label(self.frame, image=img, bg="#212121")
        panel.image = img
        panel.pack(side = TOP,pady = (0,20),padx = (0,65))

        image1 = Image.open(self.profile_image)
        image1 = image1.resize((100, 100), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(image1)
        panel1 = Label(self.frame, image=img1, bg="#212121")
        panel1.image = img1
        panel1.pack(side = TOP,pady = (0,5),padx = (0,70))
        panel1.bind('<Button-1>', self.Profile_Upload)

        username,id = self.user.split("_")
        username_label = Label(self.frame, text=username, bg="#212121", fg="#178fff")
        username_label.pack(side=TOP,pady = (0,20),padx = (0,70))


    def redirect(self):
        self.root.destroy()
        root=Tk()
        #homePage = Home_Page(root,self.dbconnection,self.user,self.friends,self.pictures,self.profile_image)
        root.mainloop()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display(self):
        image = Image.open("line.png")
        # image = image.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        panel = Label(self.frame, image=img, bg="#212121")
        panel.image = img
        panel.pack(side=TOP, pady=(0, 10), padx=(0, 65))

        user_label = Label(self.frame, text="Uploaded Images", bg="#212121", fg="#178fff")
        user_label.pack(side=TOP, pady=(0, 20), padx=(0, 70))


        pictures = self.dbconnection.retrieve_pictures(self.user)
        for picture in pictures:
            image = Image.open(picture)
            image = image.resize((300, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            panel = Label(self.frame, image=img,bg="#212121")
            panel.image = img
            panel.pack(side = TOP,padx = (0,80))

    def Upload_Event(self):
        self.filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        ticks = time.time()
        ticks = int(ticks)
        self.dbconnection.upload(self.user,self.filename,ticks)
        self.root.destroy()
        root = Tk()
        profile_obj = Profile(root, self.dbconnection, self.user, self.friends,self.pictures, self.profile_image)
        root.mainloop()


    def Profile_Upload(self,event):
        self.filename = askopenfilename()
        name = circular_image(self.filename , self.user)
        uname,id = self.user.split("_")
        self.dbconnection.editProfile(id,uname,name)
        self.root.destroy()
        root = Tk()
        profile_obj = Profile(root,self.dbconnection,self.user,self.pictures,self.friends,name)
        root.mainloop()


    def Request_Event(self):
        possible_friends= []
        friend_names = []
        for friend in self.friends:
            name,id = friend.split("_")
            self.dbconnection.retrieve_friends(self.user,id,friend_names)
        if friend_names == []:
            self.random_friends()
        else:
            i=0
            for friend in friend_names:
                if friend in self.friends or friend in possible_friends:
                    pass
                else:
                    print "Request Executed"
                    label2 = Label(self.frame, text="People Whom You May know", bg="#212121", fg="#178fff")
                    label2.pack(side=TOP, padx=(0, 70), pady=(0, 10))
                    friend_name, friend_id = friend.split("_")
                    friend_id = int(friend_id)
                    friend_profile = self.dbconnection.getProfileImage(friend_id,friend_name)
                    image1 = Image.open(friend_profile)
                    image1 = image1.resize((100, 100), Image.ANTIALIAS)
                    img1 = ImageTk.PhotoImage(image1)
                    panel1 = Label(self.frame, image=img1, bg="#212121")
                    panel1.image = img1
                    panel1.pack(side=TOP, pady=(0, 5), padx=(0, 70))

                    label = Label(self.frame, text=friend_name, bg="#212121", fg="#178fff")
                    self.Send_Request_Event_with_arg = partial(self.Send_Request_Event,friend)
                    label.pack(side=TOP, padx=(0, 70), pady=(0, 5))

                    temp = self.user + "_sent"
                    if self.dbconnection.get_request(temp,friend)==1:
                        label1 = Label(self.frame, text="Request Sent", bg="#212121", fg="#178fff")
                        label1.pack(side=TOP, padx=(0, 70), pady=(0, 10))
                    else:
                        button = Button(self.frame, text="Send", command=self.Send_Request_Event_with_arg, bg="#212121",
                                        fg="white", width=10)
                        button.pack(side = TOP,padx = (0,70), pady = (0,10))

                    image = Image.open("line.png")
                    # image = image.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(image)
                    panel = Label(self.frame, image=img, bg="#212121")
                    panel.image = img
                    panel.pack(side=TOP, pady=(0, 10), padx=(0, 65))
                    i=1
                    possible_friends.append(friend)

            if i==0:
                self.random_friends()

    def random_friends(self):
        print "random executed"
        name,id = self.user.split("_")

        rand_friends = self.dbconnection.getRandomNames(id)
        for friend in rand_friends:
            if friend in self.friends:
                pass
            else:

                label2 = Label(self.frame, text="People Whom You May know", bg="#212121", fg="#178fff")
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
                self.Send_Request_Event_with_arg = partial(self.Send_Request_Event, friend)
                label.pack(side=TOP, padx=(0, 70), pady=(0, 5))

                temp = self.user + "_sent"
                if self.dbconnection.get_request(temp, friend) == 1:
                    label1 = Label(self.frame, text="Request Sent", bg="#212121", fg="#178fff")
                    label1.pack(side=TOP, padx=(0, 70), pady=(0, 10))
                else:
                    button = Button(self.frame, text="Send", command=self.Send_Request_Event_with_arg, bg="#212121",
                                    fg="white", width=10)
                    button.pack(side=TOP, padx=(0, 70), pady=(0, 10))

                image = Image.open("line.png")
                # image = image.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)
                panel = Label(self.frame, image=img, bg="#212121")
                panel.image = img
                panel.pack(side=TOP, pady=(0, 10), padx=(0, 65))

    def View_Request_Event(self):
        label2 = Label(self.frame, text="Friend Requests", bg="#212121", fg="#178fff")
        label2.pack(side=TOP, padx=(0, 60), pady=(0, 10))
        request_string = self.user + "_request"
        friend_names = []
        self.dbconnection.get_friend_requests(request_string,friend_names)
        for friend in friend_names:
            label = Label(self.frame, text=friend, bg="#212121", fg="#178fff")
            label.pack(side=TOP, padx=(0, 70), pady=(0, 10))
            self.Accept_Request_Event_with_arg = partial(self.Accept_Request_Event,friend)

            friend_name, friend_id = friend.split("_")
            friend_id = int(friend_id)
            friend_profile = self.dbconnection.getProfileImage(friend_id, friend_name)

            image1 = Image.open(friend_profile)
            image1 = image1.resize((100, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(image1)
            panel1 = Label(self.frame, image=img1, bg="#212121")
            panel1.image = img1
            panel1.pack(side=TOP, pady=(0, 5), padx=(0, 70))

            button = Button(self.frame, text="Accept", command=self.Accept_Request_Event_with_arg,bg="#212121",
                                    fg="white", width=10)

            button.pack(side=TOP, padx=(0, 70), pady=(0, 10))



    def Accept_Request_Event(self,friend):
        name,id = self.user.split("_")
        friend_name,friend_id = friend.split("_")
        self.dbconnection.insert_friend_and_delete_request(self.user,friend,id,friend_id)
        self.root.destroy()
        root = Tk()
        self.friends.append(friend)

        profile_obj = Profile(root, self.dbconnection, self.user, self.friends,self.pictures, self.profile_image)
        root.mainloop()

    def Send_Request_Event(self,friend):
        friend_string = friend + "_request"
        friend_send_string = self.user + "_sent"
        self.dbconnection.send_request(friend_string,self.user,friend_send_string,friend)
        self.root.destroy()
        root = Tk()
        profile_obj = Profile(root, self.dbconnection, self.user, self.friends,self.pictures, self.profile_image)
        root.mainloop()