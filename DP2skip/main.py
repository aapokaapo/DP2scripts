import config
import os
from time import sleep

s = config.s


class PlayerInfo():
    def __init__(self, name, id):
        self.name = name
        self.id = id


votenumber = []
playernumber = []
maplist = []


def get_maps():
    with open(config.rotation, "r") as myfile:
        for line in myfile:
            if not line.startswith("["):
                mapname = line.replace("\n", "")
                maplist.append(mapname)


def clear_lists():
    votenumber.clear()
    playernumber.clear()
    maplist.clear()


def get_playernumber():
    players = s.get_players()
    for player in players:
        if not player.dplogin == "bot":
            playernumber.append(PlayerInfo(player.nick, player.id))


def timer():
    sleep(1)
    s.say(config.text6)
    sleep(1)
    s.say(config.text7)
    sleep(1)
    s.say(config.text8)
    sleep(1)


def voted_yes(nick):
    players = s.get_players()
    for player in players:
        if player.nick == nick:
            voting_player = player
    player_found = False
    for i in range(len(votenumber)):
        player_info = votenumber[i]
        if player_info.id == voting_player.id:
            s.say(config.text4 + voting_player.nick + " " + config.text5)
            player_found = True
    if not player_found:
        votenumber.append(PlayerInfo(voting_player.nick, voting_player.id))
        get_playernumber()
        votes_needed = int(((len(playernumber)) / 2) + 1 - len(votenumber))
        s.say(config.text3 + " " + str(votes_needed))
        playernumber.clear()


def voting_system():
    status = s.get_status()
    get_playernumber()
    if len(votenumber) > ((len(playernumber)) / 2):
        timer()
        get_maps()
        map_found = False
        for i in range(len(maplist)):
            if maplist[i] == status.get("map_name"):
                map_found = True
                mapnumber = i + 1
                if maplist[mapnumber] == "###":
                    mapnumber = 0
                print("Newmap:" + maplist[mapnumber])
                s.rcon("sv newmap " + maplist[mapnumber])
        if not map_found:
            mapnumber = 0
            print("Current map_name not in rotation,\n Newmap:" + maplist[mapnumber])
            s.rcon("sv newmap " + maplist[mapnumber])
        clear_lists()
    else:
        playernumber.clear()
        cls()


def vote(nick):
    if len(votenumber) == 0:
        s.say(config.text1)
        voted_yes(nick)
        voting_system()
    else:
        voted_yes(nick)
        voting_system()


def remove_vote(nick):
    for player in votenumber:
        if player.name == nick:
            votenumber.remove(player)
        voting_system()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("whoa's DP2skip script running! Press Ctrl+C to stop.\n")
    print("Voting timeout is " + str(config.timeout) + " seconds")
    get_playernumber()
    print("Playernumber: " + str(len(playernumber)))
    print("Votenumber: " + str(len(votenumber)))
    print("\n")
    get_maps()
    print("Map rotation:")
    status = s.get_status()
    for mapname in maplist:
        if mapname == status.get("map_name"):
            mapname = mapname + " *"
        print(str(mapname))
    print("\n")
    playernumber.clear()
    maplist.clear()
