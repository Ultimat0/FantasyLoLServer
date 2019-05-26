# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 12:37:44 2019

@author: markn
"""

import mysql.connector
import os
import hashlib
import json

connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor(buffered=True)

class User_Manager (object):
    
    def __init__ (self):
        self.current_id = 1
        
        
    #Has TODOs 
    def login (self, username, pwd):
        #Add try to check if username is even there
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        try:
            hashed = hashlib.md5(user[3].encode('latin1') + pwd.encode())
        except:
            print ("failure")
            return "Failure"
        if (hashed.hexdigest() == user[2]):
            print ("Success")
            return "Success " + str(user[0])
        else:
            print ("Failure")
            return "Failure"
            
    #MAKE DECRYPT HASH SOON        
    def create_user (self, username, pwd):
        salt = os.urandom(33)
        salted = salt + pwd.encode()
        hashed = hashlib.md5(salted)
        data = (str(self.current_id), str(username), str(hashed.hexdigest()), salt.decode('latin1'))
        cursor.execute("INSERT INTO users (idusers, username, pwd_hash, salt) VALUES (%s, %s, %s, %s)", data)
        self.current_id += 1
        
    def get_leagues_from_user (self, userId):
        ids = []
        data = {}
        cursor.execute(str("SELECT leagueId FROM middle WHERE userId=" + "'" + str(userId) + "'"))
        i = cursor.fetchone()
        while not i == None:
            print (str(i) + "!!!!!!!!!!!")
            ids.append(i)
            i = cursor.fetchone()        
        for j in ids:
            cursor.execute("SELECT league_name, id FROM leagues WHERE id=%s", (j[0],))
            temp = cursor.fetchone()
            data[temp[0]] = temp[1]
        print (json.dumps(data))
        return json.dumps(data)
    

        
    
#um.login("mark", "1234")