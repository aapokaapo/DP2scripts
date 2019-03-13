# Copyright (C) 2019  Aapo Kinnunen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
