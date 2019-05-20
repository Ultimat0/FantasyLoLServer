# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:22:48 2019

@author: markn
"""


import urllib
import ssl
from bs4 import BeautifulSoup
import mysql
import mysql.connector

connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor()

class Temp_Player(object):
    
    def __init__ (self, name_lower):
        self.name_lower = name_lower
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.csm = 0.0
        self.dpm = 0.0
        self.wpm = 0.0
        self.games = 0
        self.csm_total = 0.0
        self.dpm_total = 0.0
        self.wpm_total = 0.0
        
    def add_stats (self, kills, deaths, assists, csm, dpm, wpm):
        self.games += 1
        self.kills += kills
        self.deaths += deaths
        self.assists += assists
        self.csm_total += csm
        self.dpm_total += dpm
        self.wpm_total += wpm
        self.csm = self.csm_total / self.games
        self.dpm = self.dpm_total / self.games
        self.wpm = self.wpm_total / self.games
        
    def get_stats (self):
        return (str(self.kills), str(self.deaths), str(self.assists), str(self.csm), str(self.dpm), str(self.wpm), self.name_lower)
    
    def __str__ (self):
        return self.name_lower
        

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

players = []



for q in range(16555, 16565):

    url = "https://gol.gg/game/stats/" + str(q) + "/page-summary/"
    
    url2 = urllib.request.urlopen(url, context=ctx)
    
    soup = BeautifulSoup(url2, "html.parser")
    
    things = soup.find_all("td")
    
    #print (things)
    
    filtered = []
    final = []
            
    for thing in things:
        filtered.append(thing.text)
        final = filtered[28:len(filtered)]
        
    for i in range(len(final)):
        if i % 5 == 0:
            player = list(filter(lambda x: x.name_lower == final[i].lower(), players))
            if not len(player) == 0:
                kda_stats = final[i + 1].split("/")
                player[0].add_stats(int(kda_stats[0]), int(kda_stats[1]), int(kda_stats[2].split(" ")[0]), float(final[i + 2]), float(final[i + 3]), float(final[i + 4]))
            else:
                kda_stats = final[i + 1].split("/")
                temp = Temp_Player(final[i].lower())
                temp.add_stats(int(kda_stats[0]), int(kda_stats[1]), int(kda_stats[2].split(" ")[0]), float(final[i + 2]), float(final[i + 3]), float(final[i + 4]))
                players.append(temp)
                

for i in players:
    cursor.execute("UPDATE pros SET kills=%s, deaths=%s, assists=%s, csm=%s, dpm=%s, wpm=%s WHERE name_lower=%s", i.get_stats())

connection.commit()
print ("FINAL\n")
print (final)
    
