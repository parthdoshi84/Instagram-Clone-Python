from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import MySQLdb
import PIL
from PIL import Image, ImageTk

class dbConnection:
    def __init__(self):
        # Open database connection
        self.db = MySQLdb.connect("localhost","root","","instagram")

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def insert(self, Name, Username, Password, Country, Mobile):
        profile_picture = "default_profile.png"

        self.sql = """INSERT INTO SIGNUP(Id,Name,
                    Username, Password, Country, Mobile, Profile)
                    VALUES ('', '%s', '%s', '%s', '%s', '%s', '%s' )""" % \
                    (Name, Username, Password, Country, Mobile, profile_picture)
        try:
            self.cursor.execute(self.sql)


            self.sql = "SELECT * FROM SIGNUP WHERE Username = '%s' and Password = '%s'" % (Username, Password)
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()


            for row in self.results:
                id = row[0]
                uname = row[2]
                user = uname + "_" + str(id)

            self.sql = "CREATE TABLE `" +user+ "`(Id int(4) NOT NULL AUTO_INCREMENT , Picture VARCHAR(40) NOT NULL , Likes int(4) NOT NULL , Time int(20) NOT NULL , PRIMARY KEY (Id) )"
            self.cursor.execute(self.sql)

            self.sql = "CREATE TABLE `" + str(id) + "`(Id int(4) NOT NULL AUTO_INCREMENT , Name VARCHAR(40) NOT NULL , PRIMARY KEY (Id) )"
            self.cursor.execute(self.sql)

            request = user + "_request"
            self.sql = "CREATE TABLE `" + request + "`(Id int(4) NOT NULL AUTO_INCREMENT , Request VARCHAR(40) NOT NULL , PRIMARY KEY (Id) )"
            self.cursor.execute(self.sql)

            sent = user + "_sent"
            self.sql = "CREATE TABLE `" + sent + "`(Id int(4) NOT NULL AUTO_INCREMENT , Request VARCHAR(40) NOT NULL , PRIMARY KEY (Id) )"
            self.cursor.execute(self.sql)

            self.db.commit()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e



    def retrieve(self,Username,Password):
        self.sql = "SELECT * FROM SIGNUP WHERE Username = '%s' and Password = '%s'" % (Username,Password)
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()
            flag = 0

            for row in self.results:
                id = row[0]
                name = row[1]
                uname = row[2]
                pname = row[3]
                country = row[4]
                mobile = row[5]
                profile = row[6]
                flag = 1
                result_string = uname + "_" + str(id)
                id  = str(id)
            if flag == 1:
                self.sql = "SELECT * FROM `"+id+"`"
                self.cursor.execute(self.sql)
                # Fetch all the rows in a list of lists.
                self.results = self.cursor.fetchall()
                friend_name = []
                pictures = []
                time=[]
                for row in self.results:
                    friend_name.append(row[1])
                for friend in friend_name:
                    self.sql = "SELECT * FROM `"+friend+"`"
                    self.cursor.execute(self.sql)
                    # Fetch all the rows in a list of lists.
                    self.results = self.cursor.fetchall()
                    for row in self.results:
                        temp = row[1] + "+" + friend
                        time.append(int(row[3]))
                        pictures.append(temp)

                self.sort(pictures, time)
                return profile , result_string, friend_name , pictures
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e
        # disconnect from server

    def sort(self,pictures,time):
        for i in range(0,len(time)-1):
            for j in range(0,len(time) - i -1):
                if time[j]>time[j+1]:
                    temp = time[j]
                    time[j] = time[j+1]
                    time[j+1] = temp
                    temp = pictures[j]
                    pictures[j] = pictures[j+1]
                    pictures[j+1] = temp

    def retrieve_pictures(self,user):
        self.sql = "SELECT * FROM `" + user + "`"
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()
            pictures = []
            for row in self.results:
                pictures.append(row[1])
            return pictures
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def retrieve_friends(self, friend_original ,user,friends):
        self.sql = "SELECT * FROM `" + user + "`"
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()

            for row in self.results:
                print row[1]
                print friend_original
                if row[1]==friend_original:
                    pass
                else:
                    friends.append(row[1])
            print friends
            #return friends

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def upload(self,user,name,time):
        #self.sql = """INSERT INTO 1(Id,Name)
        #                   VALUES ('', '%s' )""" % \
        #          (name)
        print user
        self.sql  = "Insert INTO `" + user + "` Values('','%s','%d','%d')" % (name,0,time)

        try:
            self.cursor.execute(self.sql)
            self.db.commit()
            print "Success"
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e


            # disconnect from server


    def get_friend_requests(self,user,friends):
        self.sql = "SELECT * FROM `" + user + "`"
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()

            for row in self.results:
                friends.append(row[1])

            # return friends

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def insert_friend_and_delete_request(self,user,friend,user_id,friend_id):
        self.sql = "Insert INTO `" + user_id + "` Values('','%s')" % (friend)
        try:
            self.cursor.execute(self.sql)

            self.sql = "Insert INTO `" + friend_id + "` Values('','%s')" % (user)
            self.cursor.execute(self.sql)

            request_string = user + "_request"
            self.sql = "DELETE FROM `" + request_string + "` WHERE Request = '%s'" % (friend)
            self.cursor.execute(self.sql)

            sent_string = friend + "_sent"
            self.sql = "DELETE FROM `" + sent_string + "` WHERE Request = '%s'" % (user)
            self.cursor.execute(self.sql)

            print "Success"
            self.db.commit()

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def send_request(self,name,request,own, req):
        self.sql = "Insert INTO `" +name+ "` Values('','%s')" % (request)
        try:
            self.cursor.execute(self.sql)
            self.sql = "Insert INTO `" + own + "` Values('','%s')" % (req)
            self.cursor.execute(self.sql)
            self.db.commit()
            print "Success"
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e


            # disconnect from server


    def getProfileImage(self,id,uname):
        self.sql = "SELECT * FROM SIGNUP WHERE Id = '%d' and Username = '%s'" % (id, uname)
        profile = ""
        try:
            self.cursor.execute(self.sql)
            self.results = self.cursor.fetchall()


            for row in self.results:
                profile = row[6]
                return profile

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e



    def editProfile(self,id,name,profile):

        profile = str(profile)

        id= int(id)
        self.sql = "UPDATE SIGNUP SET Profile = '%s' WHERE Id = '%d'" % (profile, id)
        try:
            self.cursor.execute(self.sql)
            self.db.commit()
            print "Success"

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def get_request(self,name,friend):
        self.sql = "SELECT * FROM `" + name + "` WHERE Request = '%s'" % (friend)
        try:
            self.cursor.execute(self.sql)
            self.results = self.cursor.fetchall()

            if self.results:
                return 1
            return 0
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e

    def getRandomNames(self,own):
        names = []
        own = int(own)
        self.sql = "SELECT * FROM SIGNUP"
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()
            flag = 0

            for row in self.results:
                id = row[0]
                if own == id:
                    pass
                else:
                    uname = row[2]

                    result_string = uname + "_" + str(id)
                    names.append(result_string)
                flag = flag + 1
                if flag == 10:
                    break
            return names
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e