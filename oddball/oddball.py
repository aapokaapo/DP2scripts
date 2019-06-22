from dplib.server import Server
import threading
from time import sleep

# Config
s = Server(hostname='127.0.0.1', port=55555,
           logfile=r'/paintball2/pball/qconsole55555.log',
           rcon_password='hackme')

rotation = "/paintball2/pball/configs/rotation_oddball.txt"

holding_time = 5
# Config ends


print("whoa's oddball gamemode script running!")

s.rcon("sv forcejoin all obs")
timer = False
maplist = []
red_team = []
blue_team = []
yellow_team = []
purple_team = []
score = {"Red": 0, "Blue": 0, "Yellow": 0, "Purple": 0}
flag_holder = "none"
flag_team = "none"
round_started = False
not_dm = True


def reset():
    maplist.clear()
    red_team.clear()
    blue_team.clear()
    yellow_team.clear()
    purple_team.clear()
    global flag_holder, flag_team, round_started, timer
    flag_holder = "none"
    flag_team = "none"
    round_started = False
    timer = False
    score.clear()
    score["Red"] = 0
    score["Blue"] = 0
    score["Yellow"] = 0
    score["Purple"] = 0


def get_teams():
    status = s.get_status()
    scores = status.get("_scores")
    if colors:
        colors = scores.split()
    if colors[0].startswith("Red"):
        team1 = "Red"
    elif colors[0].startswith("Yellow"):
        team1 = "Yellow"
    elif colors[0].startswith("Purple"):
        team1 = "Purple"
    elif colors[0].startswith("Blue"):
        team1 = "Blue"
    if colors[1].startswith("Red"):
        team2 = "Red"
    elif colors[1].startswith("Yellow"):
        team2 = "Yellow"
    elif colors[1].startswith("Purple"):
        team2 = "Purple"
    elif colors[1].startswith("Blue"):
        team2 = "Blue"
    teams = [team1, team2]
    return teams


def holding_flag(nick, team):
    global flag_holder
    flag_holder = nick
    global flag_team
    flag_team = team
    try:
        score[flag_holder]
    except KeyError:
        score[flag_holder] = 0


@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon, suicide):
    global flag_holder
    if victim_nick == flag_holder:
        flag_holder = "none"
        global flag_team
        flag_team = "none"
        s.say("{C}9The flag has been dropped!")


@s.event
def on_round_end():
    global round_started
    round_started = False
    global flag_holder
    flag_holder = "none"
    global flag_team
    flag_team = "none"


def remove_player(nick):
    try:
        red_team.remove(nick)
    except ValueError:
        pass
    try:
        blue_team.remove(nick)
    except ValueError:
        pass
    try:
        yellow_team.remove(nick)
    except ValueError:
        pass
    try:
        purple_team.remove(nick)
    except ValueError:
        pass


@s.event
def on_team_switched(nick, old_team, new_team):
    global flag_holder
    if flag_holder == nick:
        flag_holder = "none"
    if new_team == "Observer":
        remove_player(nick)
    elif new_team == "Red":
        red_team.append(nick)
    elif new_team == "Blue":
        blue_team.append(nick)
    elif new_team == "Yellow":
        yellow_team.append(nick)
    elif new_team == "Purple":
        purple_team.append(nick)
    if old_team == "Red":
        red_team.remove(nick)
    elif old_team == "Blue":
        blue_team.remove(nick)
    elif old_team == "Yellow":
        yellow_team.remove(nick)
    elif old_team == "Purple":
        purple_team.remove(nick)


@s.event
def on_flag_grab(nick, flag):
    if round_started:
        for player in red_team:
            if player == nick:
                holding_flag(nick, team="Red")
        for player in blue_team:
            if player == nick:
                holding_flag(nick, team="Blue")
        for player in yellow_team:
            if player == nick:
                holding_flag(nick, team="Yellow")
        for player in purple_team:
            if player == nick:
                holding_flag(nick, team="Purple")


@s.event
def gamemode(gamemode):
    global not_dm
    global round_started
    if not gamemode == "Deathmatch":
        not_dm = True
    else:
        not_dm = False
        round_started = True


@s.event
def on_entrance(nick, build, addr):
    sleep(1)
    players = s.get_players()
    for player in players:
        if player.nick == nick:
            s.rcon("sv forcejoin " + player.id + " obs")


@s.event
def on_flag_drop(nick):
    global flag_holder
    flag_holder = "none"
    global flag_team
    flag_team = "none"
    s.say("{C}9The flag has been dropped!")


@s.event
def on_disconnect(nick):
    global flag_holder
    if flag_holder == nick:
        flag_holder = "none"
        global flag_team
        flag_team = "none"
        s.say("{C}9The flag has been dropped!")
    remove_player(nick)


@s.event
def on_round_started():
    global round_started
    round_started = True
    s.rcon("debug1 1")


@s.event
def on_mapchange(mapname):
    reset()


@s.event
def on_game_end(score_blue, score_red, score_yellow, score_purple):
    global round_started
    round_started = False
    s.rcon("debug1 0")
    teams = get_teams()
    s.say("{C}9Game ended! Scores:")
    s.say("{C}CRed: " + str(score["Red"]) + " {C}OBlue: " + str(score["Blue"]))
    s.say("{C}EYellow: " + str(score["Yellow"]) + " {C}VPurple: " + str(score["Purple"]))
    change_map()


def get_maps():  # loads the maps from rotation file
    with open(rotation, "r") as myfile:
        for line in myfile:
            if not line.startswith("["):
                mapname = line.replace("\n", "")
                maplist.append(mapname)


def change_map():  # finds the current map from maplist and changes to the one after it
    get_maps()
    map_found = False
    status = s.get_status()
    for i in range(len(maplist)):
        if maplist[i] == status.get("mapname"):
            map_found = True
            mapnumber = i + 1
            if maplist[mapnumber] == "###":
                mapnumber = 0
            print("Newmap:" + maplist[mapnumber])
            if maplist[mapnumber] == "ob/arm_ob":
                s.rcon("sv newmap " + maplist[mapnumber] + " dm")
            else:
                s.rcon("sv newmap " + maplist[mapnumber])
    if not map_found:
        mapnumber = 0
        print("Current map not in rotation,\n Newmap:" + maplist[mapnumber])
        s.rcon("sv newmap " + maplist[mapnumber])
    s.rcon("debug1 0")


def add_points():  # Checks if any team/player is holding the flag, if yes then adds point
    global timer
    if round_started:
        if not_dm:
            if not flag_team == "none":
                if flag_team == "Red":
                    color = "C"
                elif flag_team == "Blue":
                    color = "O"
                elif flag_team == "Yellow":
                    color = "E"
                elif flag_team == "Purple":
                    color = "V"
                if score[flag_team] < 50:
                    score[flag_team] += 1
                    s.say("{C}" + color + flag_team + "{C}9 team has {C}H" + str(score[flag_team]) + "{C}9 points!")
                else:
                    if not timer:
                        s.say("{C}" + color + flag_team + " has 50 points! " + flag_team + " has won!")
                        change_map()
                        timer = True
        else:
            if not flag_holder == "none":
                if flag_team == "Red":
                    color = "C"
                elif flag_team == "Blue":
                    color = "O"
                elif flag_team == "Yellow":
                    color = "E"
                elif flag_team == "Purple":
                    color = "V"
                if score[flag_holder] < 25:
                    score[flag_holder] += 1
                    s.say("{C}" + color + flag_holder + " {C}9has {C}H" + str(score[flag_holder]) + " {C}9points!")
                else:
                    if not timer:
                        s.say("{C}E" + flag_holder + "{C}9 has 25 points! " + flag_holder + " has won!")
                        change_map()
                        timer = True

    t = threading.Timer(holding_time, add_points, ())  # runs every time holding_time has passed
    t.start()


t = threading.Timer(holding_time, add_points, ())
t.start()

s.run()