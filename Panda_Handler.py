# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 18:16:56 2019

@author: markn
"""

import requests
import json
import math
import mysql.connector

connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor()

class Panda_Handler (object):
    
    def __init__ (self):
        self.current_id = 0
        self.url_endpoint = "https://api.pandascore.co"
        self.access_token = "hLodkAM1-f0ma_kqvQ4YpD3CEOFGuPSxWxaqiJOzVkJUZd9pON8"
        
    def get_all_players (self):
        cursor.execute("TRUNCATE TABLE pros")
        player_list = requests.get(self.url_endpoint + "/lol/players?page[size]=100&token=" + self.access_token, verify=False)
        total = int(player_list.headers['X-Total'])
        parsed = json.loads(player_list.content)
        #print (parsed)
        #print (str(len(parsed)) + "!!!!!")
        for i in range(len(parsed)):
            pro = parsed[i]
            if pro['current_team'] != None:
                data = (str(self.current_id), str(pro['name']), str(pro['current_team']['name']), str(pro['role']), str(pro['name']).lower(), str(pro['image_url']) if not str(pro['image_url']) == None else "None")
            else:
                data = (str(self.current_id), str(pro['name']), "None", str(pro['role']), str(pro['name']).lower(), str(pro['image_url']) if not str(pro['image_url']) == None else "None")
            cursor.execute("INSERT INTO pros (idPros, name, team, role, name_lower, image) VALUES (%s, %s, %s, %s, %s, %s)", data)
            self.current_id += 1
        for j in range(2, int(math.ceil(total/100.0))+1):
            player_list = requests.get(self.url_endpoint + "/lol/players?page[size]=100&page[number]=" + str(j) + "&token=" + self.access_token, verify=False)
            parsed = json.loads(player_list.content)
            print (parsed)
            for i in range(len(parsed)):
                pro = parsed[i]
                if pro['current_team'] != None:
                    data = (str(self.current_id), str(pro['name']), str(pro['current_team']['name']), str(pro['role']), str(pro['name']).lower(), str(pro['image_url']) if not str(pro['image_url']) == None else "None")
                else:
                    data = (str(self.current_id), str(pro['name']), "None", str(pro['role']), str(pro['name']).lower(), str(pro['image_url']) if not str(pro['image_url']) == None else "None")
                cursor.execute("INSERT INTO pros (idPros, name, team, role, name_lower, image) VALUES (%s, %s, %s, %s, %s, %s)", data)
                self.current_id += 1
        connection.commit()

        #print(parsed)
        #print (parsed[0])
        #print (player_list.json())
        
    
p = Panda_Handler()
p.get_all_players()