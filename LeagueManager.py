# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:27:07 2019

@author: markn
"""

import mysql.connector
import json

connection = mysql.connector.connect(host='localhost', database='fantasylol', user='root', password='Marknazzaro13245')

cursor = connection.cursor(buffered=True)

class League_Manager (object):
    
    def __init__ (self):
        self.current_league_id = 1
        self.current_middle_id = 1
        self.current_trades_id = 1
        
    #MAKE DECRYPT HASH SOON        
    def create_league (self, settings):
        try:
            settings_json = json.loads(settings)
            league_name = settings_json['league_name']
            ownerId = int(settings_json['owner_id'])
            team_count = settings_json['team_count']
            data = (str(self.current_league_id), str(league_name), str(ownerId), str(team_count))
            cursor.execute("INSERT INTO leagues (id, league_name, ownerId, team_count) VALUES (%s, %s, %s, %s)", data)
            connection.commit()
            data = (str(self.current_middle_id), str(ownerId), str(self.current_league_id), settings_json['team_name'], "0", "0")
            cursor.execute("INSERT INTO middle (idmiddle, userId, leagueId, team_name, wins, losses) VALUES (%s, %s, %s, %s, %s, %s)", data)
            self.current_middle_id += 1
            self.current_league_id += 1
            connection.commit()
            return "Success"
        except Exception as e:
            print (e)
            return "Failure"
    
    def add_team (self, userId, leagueId, team_name):
        data = (str(self.current_middle_id), str(userId), str(leagueId), team_name, "0", "0")
        cursor.execute("INSERT INTO middle (idmiddle, userId, leagueId, team_name, wins, losses) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.current_middle_id += 1
        connection.commit()
        return "Added player to league"
    
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
        cursor.execute("SELECT team_name, idmiddle, wins, losses, userId FROM middle WHERE leagueId=%s", (str(leagueId),))
        stuff = {}
        i = cursor.fetchone()
        while not i == None:
            stuff[i[0]] = {"team_id" : int(i[1]), "wins" : int(i[2]), "losses": int(i[3]), "user_id" : int(i[4])}
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
            
    def position_from_order(self, number):
       if number == 0:
           return "top"
       elif number == 1:
           return "jungle"
       elif number == 2:
           return "middle"
       elif number == 3:
           return "adc"
       elif number == 4:
           return "support"
       elif number == 5:
           return "bench1"
       elif number == 6:
           return "bench2"
    
    #Give me a team without all the positions that they traded and a bunch of received players
    def sort_positions(self, teamId, pros):
        cursor.execute("SELECT top, jungle, middle, adc, support, bench1, bench2 FROM middle WHERE idmiddle=%s", (str(teamId),))
        team_pros = cursor.fetchone()
        poppable_pros = pros
        once = False
        for i in range(0,7):
            once = False
            for j in range(len(poppable_pros)):
                pro = poppable_pros[j]
                print ("THIS IS A PRO: " + pro)
                print ("TEAM_PROS " + str(team_pros[i]))
                print ("Position " + self.position_from_order(i))
                cursor.execute("SELECT role FROM pros WHERE name=%s", (pro,))
                if not once and str(team_pros[i]) == "None" and (self.position_from_order(i) == str(cursor.fetchone()[0]) or (self.position_from_order(i) == "bench1" or self.position_from_order(i) == "bench2")):
                    self.add_pro_to_team(pro, teamId, self.position_from_order(i))
                    once = True
                    poppable_pros.pop(j)
        connection.commit()
                
        
    #players is a list of tuples: (player name 0, current team 1, current position 2, future team 3, future role 4) 
    def accept_trade (self, offer_json_string):
        offer = json.loads(offer_json_string)
        offered_pros = []
        requested_pros = []
        for position in offer["offer"]["offered"]:
            cursor.execute(str("SELECT " + position + " FROM middle WHERE idmiddle=" + "'" + str(offer["requesting_id"]) + "'"))
            offered_pros.append(cursor.fetchone()[0])
            cursor.execute(str("UPDATE middle SET " + position + " = NULL WHERE idmiddle=" + "'" + str(offer["requesting_id"]) +  "'"))
            connection.commit()
        for position in offer["offer"]["requested"]:
            cursor.execute(str("SELECT " + position + " FROM middle WHERE idmiddle=" + "'" + str(offer["requested_id"]) + "'"))
            requested_pros.append(cursor.fetchone()[0])
            cursor.execute(str("UPDATE middle SET " + position + " = NULL WHERE idmiddle=" + "'" + str(offer["requested_id"]) + "'"))
            connection.commit()
        print ("offered " + str(offered_pros))
        print ("requested " + str(requested_pros))
        self.sort_positions(offer["requesting_id"], requested_pros)
        self.sort_positions(offer["requested_id"], offered_pros)


    def offer_trade (self, offer_json_string):
         offer = json.loads(offer_json_string) 
         print ("OFFER: " + str(offer))
         offered_pros = {}
         requested_pros = {}
         for position in offer["offer"]["offered"]:
             cursor.execute(str("SELECT " + position + " FROM middle WHERE idmiddle='" + str(offer["requesting_id"]) + "'"))
             offered_pros[position] = cursor.fetchone()[0]
         for position in offer["offer"]["requested"]:
             cursor.execute(str("SELECT " + position + " FROM middle WHERE idmiddle='" + str(offer["requested_id"]) + "'"))
             requested_pros[position] = cursor.fetchone()[0]
         offers_json = json.dumps(offered_pros)
         requests_json = json.dumps(requested_pros)
         data = (str(self.current_trades_id), offer["requesting_id"], offer["requested_id"], json.dumps(offer), str(offers_json), str(requests_json))
         self.current_trades_id += 1
         cursor.execute("INSERT INTO trades (idtrades, requesting_team_id, requested_team_id, trade_info, offers_json, requests_json) VALUES (%s, %s, %s, %s, %s, %s)", data)
         connection.commit()
         
    def get_trades (self, teamId):
        cursor.execute("SELECT trade_info, offers_json, requests_json, requesting_team_id, requested_team_id, idtrades FROM trades WHERE requesting_team_id=%s OR requested_team_id=%s", (str(teamId), str(teamId)))
        i = cursor.fetchone()
        trades_list = []
        while not i == None:
            offers_dict = json.loads(i[1])
            requests_dict = json.loads(i[2])
            final_json_dict = {"offer" : {"offered" : offers_dict, "requested" : requests_dict}, "requesting_id" : int(i[3]), "requested_id" : int(i[4]), "trade_id" : int(i[5])}
            trades_list.append(final_json_dict)
            i = cursor.fetchone()
        print (json.dumps(trades_list))
        return json.dumps(trades_list)
        
    def get_trade (self, tradeId):
        cursor.execute("SELECT trade_info, offers_json, requests_json, requesting_team_id, requested_team_id FROM trades WHERE idtrades=%s", (str(tradeId), ))
        trade = cursor.fetchone()
        offers_dict = json.loads(trade[1])
        requests_dict = json.loads(trade[2])
        final_json_dict = {"offer" : {"offered" : offers_dict, "requested" : requests_dict}, "requesting_id" : int(trade[3]), "requested_id" : int(trade[4]), "trade_id" : int(trade[5])}
        print (json.dumps(final_json_dict))
        return json.dumps(final_json_dict)
    
    def drop_player (self, team_id, position):
        cursor.execute(str("UPDATE middle SET " + position + " = NULL WHERE idmiddle='" + str(team_id) + "'"))
        connection.commit()
    
        
    
