# DPLib - Asynchronous bot framework for Digital Paint: Paintball 2 servers
# Copyright (C) 2017  MichaÅ‚ Rokita
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
#
#Ranking system

from dplib.server import Server

s = Server(hostname='178.157.90.120', port=44444, logfile=r'/home/paintball/paintball2/pball/qconsole44444.log', rcon_password='endless')



class Player_stats():
    
    def __init__(self, name, id, kills=0, deaths=0, caps=0, pgp=0, score=0):
        self.name = name
        self.id = id
        self.kills = kills
        self.deaths = deaths
        self.caps = caps
        self.pgp = pgp
        self.score = score
    
    def add_kill(self, kills=1, score=1):
        print ('Player ' + self.name + ' got a point')
        self.kills += kills
        self.score += score
        
    def add_capture(self, caps=1, score=5):
        print ('Player ' + self.name + ' got 5 points')
        self.caps += caps
        self.score += score

    def add_death(self, deaths=1, score=1):
        print ('Player ' + self.name + ' lost a point')
        self.deaths += deaths
        self.score -= score
 
list = [Player_stats('DPBot01', 'bot')]
#@s.event
#def on_entrance(nick, build, addr):
#    players = s.get_players()
#    for player in players:
#        if player.nick == nick:
#            entered_player = player
#            break
#    player_found = False
#    for player_stats in list:
#        if entered_player.dplogin == player_stats.id:
#            player_found = True
#            player_stats.name = nick
#            print ('Player ' + player_stats.name + ' logged in')
#            print(str(list))
#            s.say ("{}: K{}/D{}/C{}/S{}".format(player_stats.name, player_stats.kills, player_stats.deaths, scoreboard.caps, scoreboard.score))
#    if not player_found:
#        list.append(Player_stats(nick, entered_player.dplogin))
#        print('Player ' +  nick + ' added to list.')
#        print(str(list))
        
def get_rank(nick):        
    print ('Player ' + nick + ' requested scoreboard')
    for player_stats in list:
    #tämä ei käy kaikki player_stats objecteja läpi listasta list
        if nick == player_stats.name:
            s.say ("{}: K{}/D{}/C{}/S{}".format(player_stats.name, player_stats.kills, player_stats.deaths, player_stats.caps, player_stats.score))
            break
        else:
            s.say ("{0} not logged in".format(nick))
            break

def get_top10():
    list.sort(reverse=True, key=lambda player_stats: player_stats.score)
    try:
        for i in range(10):
            player_stats = list[i]
            s.say("#{}:{}: Score:{}".format(i, player_stats.name, player_stats.score))
    except IndexError:
        print("Less than 10 players on list")

def add_player(nick):
    players = s.get_players()
    print("Getting playerlist")
    for player in players:
        print("Comparing nick to playerlist")
        if player.nick == nick:
            print("Found nick in playerlist")
            entered_player = player
            print("{}:{}".format(entered_player.nick, entered_player.dplogin))
            break
    player_found = False
    for player_stats in list:
        #tämä ei käy kaikkia player_stats objecteja läpi listasta list 
        print("Comparing dplogin id to player_stats.id")
        if player_stats.id == entered_player.dplogin:
            player_found = True
            print("Player {}:{} found from list!".format(nick, entered_player.dplogin))
            player_stats.name = nick
            break
        if not player_found:
            list.append(Player_stats(nick, entered_player.dplogin))
            print("Player {}:{} added to list".format(nick, entered_player.dplogin))
            break

            
@s.event
def on_chat(nick, message):
    if message == '!rank':
        get_rank(nick)
               
    if message == '!top10':
        get_top10()
     
    if message == '!addplayer':
        print("trying to add player")        
        add_player(nick)


@s.event
def on_flag_captured(team, nick, flag):
    for player_stats in list:
        if nick == player_stats.name:
            player_stats.add_capture()
            break

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    print("eliminated")
    for player_stats in list:
        if killer_nick == player_stats.name:
            player_stats.add_kill()
        if victim_nick == player_stats.name:
            player_stats.add_death()

s.run()
