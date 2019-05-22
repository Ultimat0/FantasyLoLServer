# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 08:15:01 2019

@author: markn
"""

import mysql.connector
import socket
import UserManager
import LeagueManager
import json


connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor()

s = socket.socket()
port = 25566

s.bind(('', port))         
print ("socket binded to %s" %(port))

s.listen(5)      
print ("socket is listening")        
  

"""
cursor.execute("INSERT INTO users VALUES ((0, 'Mark', 'onetwothree', 'unique')")

try:
    cursor.execute("INSERT INTO users VALUES (1, 'Misha', 'whatever', 'unique')")
except mysql.connector.errors.IntegrityError as e:
    cursor.execute("INSERT INTO users VALUES (1, 'Misha', 'whatever', 'unique2')")
    

cursor.execute("SELECT * FROM users")

print (cursor.fetchone()[3])
print (cursor.fetchone()[3])"""



class Server (object):
    
    def __init__ (self):
        cursor.execute("TRUNCATE TABLE leagues")
        cursor.execute("TRUNCATE TABLE users")
        cursor.execute("TRUNCATE TABLE middle")
        self.userManager = UserManager.User_Manager()
        self.leagueManager = LeagueManager.League_Manager()
        print ("initialized server")
        self.userManager.create_user("default", "password")
        self.userManager.create_user("default1", "password1")
        self.leagueManager.create_league(json.dumps({"league_name" : "butt", "owner_id" : 1, "team_name" : "dragons"}))
        connection.commit()
        self.leagueManager.add_team(2, 1, "tigers")
        connection.commit()
        self.run_server()
        
    def handle_incoming (self, msg):
        words = str(msg).split(" ")
        words[0] = words[0][2:len(words[0])]
        words[-1] = words[-1][0:len(words[-1]) - 1]
        print (words)
        if words[0] == "create_user":
            self.userManager.create_user(words[1], words[2])
            print ("creating user")
            return bytes("creating user", "utf-8")
        elif words[0] == "login":
            print ("trying log in")
            return bytes(self.userManager.login(words[1], words[2]), "utf-8")
        elif words[0] == "create_league":
            print ("creating league")
            return bytes(self.leagueManager.create_league(words[1], words[2], words[3]), "utf-8")
        elif words[0] == "get_users_from_league":
            print ("getting users from league")
            return bytes(str(self.leagueManager.get_users_from_league(words[1])), "utf-8")
        elif words[0] == "get_leagues_from_user":
            print ("getting leagues from user")
            return bytes(str(self.userManager.get_leagues_from_user(words[1])), "utf-8")
        elif words [0] == "get_teams_from_league":
            print ("getting teams from league")
            return bytes(str(self.leagueManager.get_teams_from_league(words[1])), "utf-8")
        elif words [0] == "get_free_agents_from_league":
            print ("getting free agents from league")
            return str(self.leagueManager.get_free_agents(words[1]))
        elif words [0] == "add_pro_to_team":
            print ("adding pro to team")
            return bytes(str(self.leagueManager.add_pro_to_team(words[1], words[2], words[3])), "utf-8")
        elif words [0] == "get_pros_from_team":
            print ("getting pros from team")
            return bytes(str(self.leagueManager.get_pros_from_team(words[1])), "utf-8")
        elif words [0] == "get_pro_info":
            print ("getting pro info")
            return bytes(str(self.leagueManager.get_pro_info(words[1])), "utf-8")
        return bytes("rip 1", "utf-8")
        
    def run_server (self):
        while True: 
            # Establish connection with client. 
            c, addr = s.accept()     
            msg = c.recv(4096)
            print ('Got connection from', addr)
            print (msg)
            incoming = self.handle_incoming(msg)
            if len(incoming) > 4096:
                buffer = ""
                count = 0
                for i in incoming:
                    if count > 4095:
                        c.send(bytes(buffer, "utf-8"))
                        buffer = ""
                        count = 0
                    buffer += i
                    count += 1
                c.send(bytes(buffer, "utf-8"))
            else:
                c.send(incoming)
            c.close()
    
server = Server()


"""while True: 
   # Establish connection with client. 
   c, addr = s.accept()     
   msg = c.recv(4096)
   print ('Got connection from', addr)
   print (msg)
   
   
   server.handle_incoming(msg)
       
  
   # send a thank you message to the client.  
   c.send(bytes("Thanks", 'utf-8')) 
  
   # Close the connection with the client 
   c.close() """

#server.userManager.create_user("mark", "1234")

