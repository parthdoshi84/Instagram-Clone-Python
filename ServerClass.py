import socket
import thread
import threading
import MySQLdb

class dbConnection:
    def __init__(self):
        # Open database connection
        self.db = MySQLdb.connect("localhost","root","","instagram")

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def insert(self, Name, Username, Password, Country, Mobile):


        self.sql = """INSERT INTO SIGNUP(Id,Name,
                    Username, Password, Country, Mobile)
                    VALUES ('', '%s', '%s', '%s', '%s', '%s' )""" % \
                    (Name, Username, Password, Country, Mobile)
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Commit your changes in the database
            self.db.commit()
            print "Success"
        except:
            # Rollback in case there is any error
            self.db.rollback()
            print "Did not work"

        # disconnect from server
        self.db.close()

    def retrieve(self,Username,Password):
        self.sql = "SELECT * FROM SIGNUP WHERE Username = '%s' and Password = '%s'" % (Username,Password)
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            self.results = self.cursor.fetchall()
            flag = 0

            for row in self.results:
                print "Inside row"
                id = row[0]
                name = row[1]
                uname = row[2]
                pname = row[3]
                country = row[4]
                mobile = row[5]
                flag = 1
                result_string = name + "+" + uname + "+" + pname + "+" + country + "+" + "mobile"
                id  = str(id)
                print id
                print type(id)
            if flag == 1:
                print "Inside flag"
                self.sql = 'SELECT * FROM ' +id
                self.cursor.execute(self.sql)
                # Fetch all the rows in a list of lists.
                self.results = self.cursor.fetchall()
                print "Worked"
                friend_name = []
                pictures = ""
                for row in self.results:
                    friend_name.append(row[1])
                for friend in friend_name:
                    self.sql = "SELECT * FROM '%s'" % (friend)
                    self.cursor.execute(self.sql)
                    # Fetch all the rows in a list of lists.
                    self.results = self.cursor.fetchall()
                    print "Pictures"
                    for row in self.results:
                        pictures = pictures + '+' + row[1]
                print pictures
                return pictures
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print e
        # disconnect from server
        self.db.close()

    def upload(self,Name):
        self.sql = """INSERT INTO 1(Id,Name)
                           VALUES ('', '%s' )""" % \
                   (Name)

        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            # Commit your changes in the database
            self.db.commit()
            print "Success"
        except:
            # Rollback in case there is any error
            self.db.rollback()
            print "Did not work"

            # disconnect from server
        self.db.close()




class ServerThread(threading.Thread):
    def __init__(self,sockpy,sockets):
        super(ServerThread,self).__init__()
        self.sockpy = sockpy
        self.sockets = sockets

    """def run(self):
        while True:
            message = self.sockpy.recv(1024)

            for index, socketed in enumerate(self.sockets):
                if socketed == self.sockpy:
                    pass
                    #message = "Client " + str(index) + " " + message
            for socket in self.sockets:
                if socket != self.sockpy:
                    socket.send(message)
    """
    def run(self):
        while True:
            print "Ready to recieve"
            string  = self.sockpy.recv(1024)
            dbconnection = dbConnection()
            if '+' in string:
                info = string.split('+')

                result  = dbconnection.retrieve(info[0],info[1])
                for socket in self.sockets:
                    print result
                    if socket == self.sockpy:
                        socket.send(result)
            else:
                result =  dbconnection.upload(string)
class Server(threading.Thread):
    def __init__(self):
        super(Server,self).__init__()

    def run(self):
        sockpy = socket.socket()
        host = 'localhost'
        port = 12345
        sockpy.bind((host,port))
        sockpy.listen(5)
        sockets = []

        while True:
            c, address = sockpy.accept()
            print "Client Arrived"
            sockets.append(c)

            serverthread = ServerThread(c,sockets)
            serverthread.start()
        c.close()
        sockpy.close()


serverSocket = Server()
serverSocket.start()













