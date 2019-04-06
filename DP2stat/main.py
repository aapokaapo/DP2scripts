from playerstats import PlayerStats
import config

winner = ""

s =config.s

player_list = [PlayerStats('DPBot01', 'bot')]

def last_month_winner():
    with open(config.savefile2, "r") as myfile:
        for line in myfile:
            if not line.startswith("#"):
                break
        global winner
        line = line.split()
        winner = line[6]
        print("Last months winner:" + winner)

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
            player_stats.name = nick
            player_found = True
            print(player_stats.name + " already on Leaderboard(TM)")
    if not player_found:

        if entered_player.dplogin == "":
            print(entered_player.nick + " doesn't have dplogin, stats won't be tracked")
        elif entered_player.dplogin == "bot":
            print("DP2Leaderboard(TM) is not for bots")
        else:
            player_list.append(PlayerStats(nick, entered_player.dplogin))
            print("Player {}:{} added to Leaderboard(TM)".format(
                nick, entered_player.dplogin))
 
def stats_reset():
    for player in player_list:
        player.kills = 0
        player.deaths = 0
        player.caps = 0
        player.grabs = 0
    last_month_winner()
    print("stats reseted")
    
def get_help():
    s.say("{C}DYou must have a Global Login account to use DP2Leaderboard(TM)")
    s.say("{C}DType {C}?!stats {C}Dto see your current stats")
    s.say("{C}DType {C}?!top10 {C}Dto see current top10")
    s.say("{C}DType {C}?!top10kd {C}Dto see current top10 on K/D-ratio")
    s.say("{C}DPlayer can use each command once/map!")

def get_top10():
    player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
    try:
        for i in range(10):
            player_stats = player_list[i]
            player_index = i + 1
            score = (player_stats.kills - player_stats.deaths + 3*player_stats.grabs + 5*player_stats.caps)
            if player_stats.id == winner:
                s.say("{C}D#" + str(player_index)
                    +" {C}O" + player_stats.name
                    + ":{C}LK:" + str(player_stats.kills)
                    + "{C}0/{C}BD:" + str(player_stats.deaths)
                    + "{C}0/{C}LS:" + str(score)
                    )
            else:
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
            if player_stats.id == winner:
                s.say("{C}D#" + str(player_index)
                    +" {C}O" + player_stats.name
                    + ":{C}LK:" + str(player_stats.kills)
                    + "{C}0/{C}BD:" + str(player_stats.deaths)
                    + "{C}0/{C}OK/D:" + str(kd)
                    )
            else:
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
            if player_stats.id == winner:
                s.say("{C}D#" + str(player_index)
                    + " {C}O" + player_stats.name
                    + ":{C}LK:" + str(player_stats.kills)
                    + "{C}0/{C}BD:"+ str(player_stats.deaths)
                    + "{C}0/{C}LC:"+ str(player_stats.caps)
                    + "{C}0/{C}LG:" + str(player_stats.grabs)
                    + "{C}0/{C}LS:" + str(score)
                    + "{C}0/{C}OK/D:" + str(kd)
                    )
                player_found = True
                break
            else:
                s.say("{C}D#" + str(player_index)
                    + " " + player_stats.name
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
        s.say("{0} nickname not registered on DP2Leaderboard(TM). Type !addplayer".format(nick))
        
def leaderboard_save():
    with open(config.savefile, 'w') as myfile:
        myfile.write("# DP2Stats Leaderboard\n# RANK K/D K D C G ID NAME\n")
        print("Map changed. Leaderboard saved.") 
        player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
        for i in range(len(player_list)):
            player_index = i + 1
            player_stats = player_list[i]
            deaths = player_stats.deaths
            if deaths == 0:
                kd = round((float(player_stats.kills)/int(1)), 3)
            else:
                kd = round((float(player_stats.kills)/float(player_stats.deaths)), 3)
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
                    print(nick +" "+ id)
            print("player_list loaded")
            s.say("{C}0***{C}CLeaderboard loaded{C}0***")
    except FileNotFoundError:
        print("No savefile yet")
