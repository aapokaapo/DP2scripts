from dplib.server import Server
from time import sleep

# Define the portnumber, logfile and rcon_password
s = Server(hostname='127.0.0.1', port=11111,
           logfile=r'/home/paintball/paintball2/pball/qconsole11111.log',
           rcon_password='whoaisbest')

rotation = "pball/configs/rotation2.txt"


class PlayerInfo():
    def __init__(self, name, id):
        self.name = name
        self.id = id

votenumber = []
playernumber = []
maplist = []

def clear_lists():
    votenumber.clear()
    playernumber.clear()
    maplist.clear()
    
def get_playernumber():
    players = s.get_players()
    for player in players:
        if not player.dplogin == "bot":
            playernumber.append(PlayerInfo(player.nick, player.id))
    print("Playernumber:")
    print(len(playernumber))
    
def timer():
    sleep(1)
    s.say("Skip vote passed! Map will be changed! in 5")
    sleep(1)
    s.say("Map will be changed in 4")
    sleep(1)
    s.say("Map will be changed in 3")
    sleep(1)
    s.say("Map will be changed in 2")
    sleep(1)
    s.say("Map will be changed in 1")
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
            s.say(voting_player.nick + " already voted yes!")
            player_found = True
    if not player_found:
        votenumber.append(PlayerInfo(voting_player.nick, voting_player.id))
        s.say(voting_player.nick + " voted yes!")
   
def voting_system():
    status = s.get_status()
    get_playernumber()
    print("Votenumber:")
    print(len(votenumber))
    if len(votenumber) > ((len(playernumber))/2):
        timer()
        with open(rotation, "r") as myfile:
            for line in myfile:
                if not line.startswith("["):
                    mapname =line.replace("\n", "")
                    maplist.append(mapname)
        print(str(maplist))
        map_found = False
        for i in range(len(maplist)):
            if maplist[i] == status.get("mapname"):
                map_found = True
                mapnumber = i + 1
                if maplist[mapnumber] == "###":
                    mapnumber = 0
                print("Newmap:" + maplist[mapnumber])
                s.rcon("gamemap " + maplist[mapnumber])
        if not map_found:
            mapnumber = 0
            print("Map not in rotation, Newmap:" + maplist[mapnumber])
            s.rcon("gamemap " + maplist[mapnumber])
        clear_lists()
    else:
        playernumber.clear()
        

            
@s.event   
def on_chat(nick, message):
    if message == '!skip':
        s.rcon("sv_consolename 1")
        if len(votenumber) == 0:
            s.say("Vote to skip map requested! To vote yes type '!skip'")
            voted_yes(nick)
            voting_system()
        else:
            voted_yes(nick)
            voting_system()
        
s.run()