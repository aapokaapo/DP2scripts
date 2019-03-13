from playerstats import PlayerStats
import config

s =config.s

player_list = [PlayerStats('DPBot01', 'bot')]

def add_player(nick):
    players = s.get_players()
    for player in players:
        if player.nick == nick:
            entered_player = player
            break
    player_found = False
    for i in range(len(player_list)):
        player_stats = player_list[i]
        if player_stats.id == entered_player.dplogin:
            s.say("{C}C***Player " + nick + ":" + entered_player.dplogin + " already on DP2Leaderboard(TM)***")
            player_stats.name = nick
            player_found = True
            print(player_stats.name + " already on Leaderboard(TM)")
    if not player_found:

        if entered_player.dplogin == "":
            s.say("{C}C!!!WARNING " + nick + " does not have Global Login id, please login!!!")
        else:
            player_list.append(PlayerStats(nick, entered_player.dplogin))
            print("Player {}:{} added to Leaderboard(TM)".format(
                nick, entered_player.dplogin))
            s.say("{C}C***Player " + nick + ":" + entered_player.dplogin + " added to DP2Leaderboard(TM)***")

def get_help():
    s.say("{C}DType {C}?!stats {C}Dto see your current stats")
    s.say("{C}DType {C}?!top10 {C}Dto see current top10")
    s.say("{C}DType {C}?!top10kd {C}Dto see current top10 on K/D-ratio")
    s.say("{C}DType {C}?!addplayer {C}Dto add yourself to the leaderboard")
    s.say("{C}DYou must have a Global Login account to use DP2Leaderboard(TM)")

def get_top10():
    player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
    try:
        for i in range(10):
            player_stats = player_list[i]
            player_index = i + 1
            score = (player_stats.kills - player_stats.deaths + 3*player_stats.grabs + 5*player_stats.caps)
            s.say("{C}D#" + str(player_index)
                +" {C}D" + player_stats.name
                + ":{C}LK:" + str(player_stats.kills)
                + "{C}0/{C}BD:" + str(player_stats.deaths)
                + "{C}0/{C}LS:" + str(score)
                )
    except IndexError:
        print("Less than 10 players on Leaderboard")
        
def get_top10kd():
    try:
        player_list.sort(reverse=True, key=lambda player_stats: float(player_stats.kills)/float(player_stats.deaths))
    except ZeroDivisionError:
        player_list.sort(reverse=True, key=lambda player_stats: float(player_stats.kills)/float(player_stats.deaths+1))
    try:
        for i in range(10):
            player_stats = player_list[i]
            player_index = i + 1
            deaths = player_stats.deaths
            if deaths == 0:
                kd = "{:0.2f}".format(float(player_stats.kills)/int(1))
            else:
                kd = "{:0.2f}".format(float(player_stats.kills)/float(player_stats.deaths))
            s.say("{C}D#" + str(player_index)
                +" {C}D" + player_stats.name
                + ":{C}LK:" + str(player_stats.kills)
                + "{C}0/{C}BD:" + str(player_stats.deaths)
                + "{C}0/{C}OK/D:" + str(kd)
                )
    except IndexError:
        print("Less than 10 players on Leaderboard")

def get_stats(nick):
    player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
    print('Player ' + nick + ' requested his stats')
    for i in range(len(player_list)):
        player_index = i + 1
        player_stats = player_list[i]
        score = (player_stats.kills - player_stats.deaths + 3*player_stats.grabs + 5*player_stats.caps)
        deaths = player_stats.deaths
        if deaths == 0:
            kd = "{:0.2f}".format(float(player_stats.kills)/int(1))
        else:
            kd = "{:0.2f}".format(float(player_stats.kills)/float(player_stats.deaths))
            
        player_found = False
        if player_stats.name == nick:
            s.say("{C}A#" + str(player_index)
                + " {C}E" + player_stats.name
                + ":{C}LK:" + str(player_stats.kills)
                + "{C}0/{C}BD:"+ str(player_stats.deaths)
                + "{C}0/{C}LC:"+ str(player_stats.caps)
                + "{C}0/{C}LG:" + str(player_stats.grabs)
                + "{C}0/{C}LS:" + str(score)
                + "{C}0/{C}OK/D:" + str(kd)
                )
            player_found = True
            break
    if not player_found:
        s.say("{0} nickname not registered on Leaderboard(TM). Type !addplayer".format(nick))
        
def leaderboard_save():
    with open(config.savefile, 'w') as myfile:
        myfile.write("# DP2RankingSystem Leaderboard\n# RANK K/D K D C G ID NAME\n")
        print("Map changed. Leaderboard saved.") 
        player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
        for i in range(len(player_list)):
            player_index = i + 1
            player_stats = player_list[i]
            deaths = player_stats.deaths
            if deaths == 0:
                kd = (float(player_stats.kills)/int(1))
            else:
                kd = (float(player_stats.kills)/float(player_stats.deaths))
            myfile.write(str(player_index) + " "
                + str(kd) + " "
                + str(player_stats.kills) + " "
                + str(player_stats.deaths) + " "
                + str(player_stats.caps) + " "
                + str(player_stats.grabs) + " "
                + str(player_stats.id) + " "
                + player_stats.name + "\n")
    s.say("{C}0***{C}CLeaderboard saved{C}0***")
        
def leaderboard_load():
    try:
        player_list.clear()
        with open(config.savefile, 'r') as myfile:
            for line in myfile:
                if not line.startswith("#"):
                    saved_player = line.split()
                    nick = saved_player[7]
                    kills = int(saved_player[2])
                    deaths = int(saved_player[3])
                    caps = int(saved_player[4])
                    grabs = int(saved_player[5 ])
                    id = saved_player[6]
                    player_list.append(PlayerStats(nick, id, kills, deaths, caps, grabs))
                    s.say(nick +" "+ id)
            print("player_list loaded")
            s.say("{C}0***{C}CLeaderboard loaded{C}0***")
    except FileNotFoundError:
        print("No savefile yet")
