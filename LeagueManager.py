# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:27:07 2019

@author: markn
"""

import mysql.connector
import json

connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor()

class League_Manager (object):
    
    def __init__ (self):
        self.current_league_id = 1
        self.current_middle_id = 1
        
    #MAKE DECRYPT HASH SOON        
    def create_league (self, settings):
        settings_json = json.loads(settings)
        league_name = settings_json['league_name']
        ownerId = int(settings_json['owner_id'])
        team_name = settings_json['team_name']
        data = (str(self.current_league_id), str(league_name), str(ownerId))
        cursor.execute("INSERT INTO leagues (id, league_name, ownerId) VALUES (%s, %s, %s)", data)
        data = (str(self.current_middle_id), str(ownerId), str(self.current_league_id), team_name, "0", "0")
        cursor.execute("INSERT INTO middle (idmiddle, userId, leagueId, team_name, wins, losses) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.current_league_id += 1
        self.current_middle_id += 1
        connection.commit()
        return "Created league"
    
    def add_team (self, userId, leagueId, team_name):
        data = (str(self.current_middle_id), str(userId), str(leagueId), team_name, "0", "0")
        cursor.execute("INSERT INTO middle (idmiddle, userId, leagueId, team_name, wins, losses) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.current_middle_id += 1
        return "Added player to league"
    
    def get_users_from_league (self, leagueId):
        ids = []
        data = {}
        cursor.execute("SELECT userId FROM middle WHERE leagueId=%s", (str(leagueId),))
        i = cursor.fetchone()
        while not i == None:
            print (i)
            ids.append(i)
            i = cursor.fetchone()
        
        for j in ids:
            cursor.execute("SELECT username, idusers FROM users WHERE idusers=%s", (j[0],))
            temp = cursor.fetchone()
            data[temp[0]] = temp[1]
        print (json.dumps(data))
        return json.dumps(data)
    
    def get_teams_from_league (self, leagueId):
        cursor.execute("SELECT team_name, idmiddle, wins, losses FROM middle WHERE leagueId=%s", (str(leagueId),))
        stuff = {}
        i = cursor.fetchone()
        while not i == None:
            stuff[i[0]] = (i[1], int(i[2]), int(i[3]))
            i = cursor.fetchone()
        print (json.dumps(stuff))
        return json.dumps(stuff)
    
    #TODO: Make more efficient (super slow my goodness)
    def get_free_agents (self, leagueId):
        not_free = []
        cursor.execute("SELECT top, middle, adc, support, jungle, bench1, bench2 FROM middle WHERE leagueId=%s", (str(leagueId),))
        i = cursor.fetchone()
        while not i == None:
            for pro in i:
                if not pro == None:
                    not_free.append(pro)
            i = cursor.fetchone()
        cursor.execute("SELECT name, image, kills, deaths, assists, team, role FROM pros")
        frees = list(filter(lambda x: x[0] not in not_free, cursor.fetchall()))
        stuff = {}
        for free in frees:
            stuff[free[0]] = {"image" : free[1], "team" : str(free[5]), "role" : str(free[6]), "kills" : str(free[2]), "deaths" : str(free[3]), "assists" : str(free[4])}        
        print (json.dumps(stuff))
        return json.dumps(stuff)
    
    
    def add_pro_to_team (self, pro_name, middle_id, position):
        if position == "top":
            cursor.execute("UPDATE middle SET top=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "jungle":
            cursor.execute("UPDATE middle SET jungle=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "middle":
            cursor.execute("UPDATE middle SET middle=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "adc":
            cursor.execute("UPDATE middle SET adc=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "support":
            cursor.execute("UPDATE middle SET support=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "bench1":
            cursor.execute("UPDATE middle SET bench1=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        elif position == "bench2":
            cursor.execute("UPDATE middle SET bench2=%s WHERE idmiddle=%s", (pro_name, str(middle_id)))
        result = "Added " + pro_name + " to " + str(middle_id)
        connection.commit()
        print (result)
        return result
    
    def get_pro_info (self, pro_name):
        cursor.execute ("SELECT team, role, image, kills, deaths, assists, csm, dpm, wpm FROM pros WHERE name=%s", (pro_name,))
        pro = cursor.fetchone()
        stuff = {"team" : str(pro[0]), "role" : str(pro[1]), "image" : str(pro[2]), "kills" : str(pro[3]), "deaths" : str(pro[4]), "assists" : str(pro[5]), "csm" : str(pro[6]), "dpm" : str(pro[7]), "wpm" : str(pro[8])} 
        print (json.dumps(stuff))
        return json.dumps(stuff)
    
    def get_pros_from_team (self, middle_id):
        cursor.execute("SELECT top, jungle, middle, adc, support, bench1, bench2 FROM middle WHERE idmiddle=%s", (str(middle_id),))
        players = {}
        for team in cursor.fetchall():
            count = 1
            for player in team:
                if count == 1:
                    role = "top"
                elif count == 2:
                    role = "jungle"
                elif count == 3:
                    role = "middle"
                elif count == 4:
                    role = "adc"
                elif count == 5:
                    role = "support"
                elif count == 6:
                    role = "bench 1"
                elif count == 7:
                    role = "bench 2"
                if not player == None:
                    cursor.execute("SELECT image, team, role, kills, deaths, assists FROM pros WHERE name=%s", (player,))
                    temp = cursor.fetchone()
                    players[player] = {"image" : temp[0], "team" : temp[1], "role" : role, "kills" : temp[3], "deaths" : temp[4], "assists" : temp[5]}
                count += 1
        print (json.dumps(players))
        return json.dumps(players)
            
    
    """ #players is a list of tuples: (player name 0, current team 1, current position 2, future team 3, future role 4)
    def trade (self, *players):
        for player in players: """
        
        
        
            
        
        
    
        
    
