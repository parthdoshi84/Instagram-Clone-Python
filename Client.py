import socket
import thread
import threading
from Tkinter import *

class clientClass(threading.Thread):
    def __init__(self,sockpy,username,password):
        super(clientClass,self).__init__()
        self.sockpy = sockpy
        self.username = username
        self.password = password

    def run(self):
        #input  = raw_input("Enter input")
        string  = self.username + "+"  + self.password
        self.sockpy.send(string)
        '''f = open("Client1/events.jpg","rb")
        while True:
            l = f.read(1024)
            while (l):
                print 'Sending...'
                self.sockpy.send(l)
                l = f.read(1024)
        f.close()
        '''

class Profile:
    def __init__(self, root):
        # widgets
        self.file = Label(root, text="File")
        self.file_entry = Entry(root)
        self.upload = Button(root, text="Upload", command=self.Upload_Event)

        # position
        self.file.grid(row = 0, column = 0)
        self.file_entry.grid(row = 0, column = 1)
        self.upload.grid(row=1, column=1)

    def Upload_Event(self):




class Client(threading.Thread):
    def __init__(self,username,password):
        super(Client,self).__init__()
        self.username = username
        self.password = password
        self.result = ""

    def print_result(self):
        return self.result

    def run(self):
        sockpy = socket.socket()
        host = 'localhost'
        port = 12345
        sockpy.connect((host, port))


        clientclass = clientClass(sockpy,self.username,self.password)
        clientclass.start()

        root = Tk()
        profile = Profile(root)
        root.mainloop()

        while True:
            l = sockpy.recv(1024)
            self.result = l
            print self.result
            '''f = open("Client2/event.jpg", "wb")
            while (l):
                print "Receiving..."
                f.write(l)
                l = sockpy.recv(1024)
        f.close()'''

            #message = sockpy.recv(1024)
            #print message
        sockpy.close()












