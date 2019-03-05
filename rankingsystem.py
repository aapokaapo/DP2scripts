from dplib.server import Server
from time import sleep
import threading

s = Server(hostname='127.0.0.1', port=22222,
           logfile=r'/home/user/paintball2/pball/qconsole22222.log',
           rcon_password='hackme')


print("ServerSide DP2RankingSystem running. Made by whoa")

class PlayerStats():

    def __init__(self, name, id, kills=0, deaths=0, caps=0, grabs=0):
        self.name = name
        self.id = id
        self.kills = kills
        self.deaths = deaths
        self.caps = caps
        self.grabs = grabs

    def add_kill(self, kills=1):
        print('Player ' + self.name + ' got a point')
        self.kills += kills
            
    def add_capture(self, caps=1):
        print('Player ' + self.name + ' captured the flag')
        self.caps += caps

    def add_death(self, deaths=1):
        print('Player ' + self.name + ' died')
        self.deaths += deaths
            
    def add_grab(self, grabs=1):
        print('Player ' + self.name + ' got a grab')
        self.grabs += grabs
        
        
player_list = [PlayerStats('DPBot01', 'bot')]

def no_division_by_zero(player):
    if player.deaths = 0:
        n = 1
    else:
        n = 0
    return n

def add_player(nick):
    print("Trying to add player")
    players = s.get_players()
    print("Getting in-game playerlist with GL id's")
    for player in players:
        print("Comparing in-game playerlist nick to the message senders nick")
        if player.nick == nick:
            print("Found senders nick in in-game playerlist")
            entered_player = player
            print(entered_player.nick + " : " + entered_player.dplogin)
            break
    player_found = False
    for i in range(len(player_list)):
        player_stats = player_list[i]
        print("Comparing dplogin id to already registered id's")
        print("player_list:#{}:{}:{}".format(i, player_stats.name, player_stats.id))
        print("Trying to add:{}:{}".format(
            entered_player.nick, entered_player.dplogin))
        if player_stats.id == entered_player.dplogin:
            print("Player {}:{} found from Leaderboard!".format(
                nick, entered_player.dplogin))
            s.say("Player " + nick + ":" + entered_player.dplogin + " found from leaderboard")
            player_stats.name = nick
            player_found = True
    if not player_found:
        
        if entered_player.dplogin == "":
            s.say("{C}C!!!WARNING!!! " + nick + " {C}Cdoes not have Global Login id, please login")
        else:
            player_list.append(PlayerStats(nick, entered_player.dplogin))
            print("Player {}:{} added to player_list".format(
                nick, entered_player.dplogin))
            s.say("Player " + nick + ":" + entered_player.dplogin + " added to leaderboard")
        
        
def get_top10():
    for e in range(len(player_list)):
        player_stats = player_list[e]
        n = no_division_by_zero(player_stats)
    player_list.sort(reverse=True, key=lambda player_stats: float(player_stats.kills)/float(player_stats.deaths + n))
    try:
        for i in range(10):
            player_stats = player_list[i]
            n = no_division_by_zero(player_stats)
            player_index = i + 1
            s.say("#" + str(player_index) 
                +" {C}E" + player_stats.name 
                + ":{C}LK:" + str(player_stats.kills) 
                + "{C}0/{C}BD:" + str(player_stats.deaths) 
                + "{C}0/{C}OK/D:" + str(round(player_stats.kills/(player_stats.deaths +n) ,2))
                )
    except IndexError:
        print("Less than 10 players on Leaderboard")
        
def get_stats(nick):
    for e in range(len(player_list)):
        player_stats = player_list[e]
        n = no_division_by_zero(player_stats)
    player_list.sort(reverse=True, key=lambda player_stats: float(player_stats.kills)/float(player_stats.deaths + n))
    print('Player ' + nick + ' requested his stats')
    for i in range(len(player_list)):
        player_index = i + 1
        player_stats = player_list[i]
        n = no_division_by_zero(player_stats)
        player_found = False
        if player_stats.name == nick:
            s.say("{C}A#" + str(player_index) 
                + " {C}E" + player_stats.name 
                + ":{C}LK:" + str(player_stats.kills) 
                + "{C}0/{C}BD:"+ str(player_stats.deaths) 
                + "{C}0/{C}LC:"+ str(player_stats.caps) 
                + "{C}0/{C}LG:" + str(player_stats.grabs) 
                + "{C}0/{C}OK/D:" + str(round(player_stats.kills/(player_stats.deaths + n),2)) )
            player_found = True
            break
    if not player_found:
        s.say("{0} nickname not registered on Leaderboard(TM). Type !addplayer".format(nick))
       
def save_leaderboard(nick):
    filename = "/var/www/html/whoa.ga/feedback/leaderboard.txt"
    if nick == "whoa":
        with open(filename, 'w') as myfile:
            print("whoa used op power to save leaderboard")
            for e in range(len(player_list)):
                player_stats = player_list[e]
                n = no_division_by_zero(player_stats)
            player_list.sort(reverse=True, key=lambda player_stats: float(player_stats.kills)/float(player_stats.deaths + n))
            for i in range(len(player_list)):
                player_index = i + 1
                player_stats = player_list[i]
                n = no_division_by_zero(player_stats)
                s.say(str(player_index) + " " 
                    + str(float(player_stats.kills)/(float(player_stats.deaths +n))) + " " 
                    + str(player_stats.kills) + " " 
                    + str(player_stats.deaths) + " "
                    + str(player_stats.caps) + " " 
                    + str(player_stats.grabs) + " "
                    + str(player_stats.id) + " " 
                    + player_stats.name)
                myfile.write(str(player_index) + " " 
                    + str(float(player_stats.kills)/(float(player_stats.deaths +n))) + " " 
                    + str(player_stats.kills) + " " 
                    + str(player_stats.deaths) + " "
                    + str(player_stats.caps) + " " 
                    + str(player_stats.grabs) + " "
                    + str(player_stats.id) + " " 
                    + player_stats.name + "\n")
        s.say("{C}0***{C}CLeaderboard save{C}0***")

                

def load_leaderboard(nick):
    filename = "/var/www/html/whoa.ga/feedback/leaderboard.txt"
    if nick == "whoa":
        player_list.clear()
        player_stats = PlayerStats
        with open(filename, 'r') as myfile:
            while True:
                line = myfile.readline()
                if not line:
                    break            
                saved_player = line.split()
                player_stats.name = saved_player[7]
                player_stats.kills = int(saved_player[2])
                player_stats.deaths = int(saved_player[3])
                player_stats.caps = int(saved_player[4])
                player_stats.grabs = int(saved_player[5 ])
                player_stats.id = saved_player[6]
                player_list.append(player_stats)
            print("player_list loaded")
            print(player_list)

def debug1(nick):
    if nick == "whoa":
        print(player_list)
        
@s.event
def on_chat(nick, message):
    if message == '!stats':
        get_stats(nick)

    if message == '!top10':
        get_top10()

    if message == '!addplayer':
        add_player(nick)

    if message == '!save':
        save_leaderboard(nick)
    
    if message == '!load':
        load_leaderboard(nick)
        
    if message == '!debug1':
        debug1(nick)
            
@s.event
def on_flag_captured(team, nick, flag):
    for player_stats in player_list:
        if nick == player_stats.name:
            player_stats.add_capture()
            break

@s.event
def on_elim_teams_flag(team, nick, points):
    for player_stats in player_list:
        if nick == player_stats.name:
            player_stats.add_grab()
            break   

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    print("elimination")
    for player_stats in player_list:
        if killer_nick == player_stats.name:
            player_stats.add_kill()
        if victim_nick == player_stats.name:
            player_stats.add_death()
            
def infomessage():
    s.say("{C}DTo add yourself to leaderboard, type !addplayer")
    sleep(60)
    s.say("{C}DTo see your stats type !stats")
    t = threading.Timer(300.0, infomessage,())
    t.start()
t = threading.Timer(300.0, infomessage,())
t.start()

s.run()
            
