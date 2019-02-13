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

from dplib.server import Server
import numpy as np

s = Server(hostname='178.157.90.120', port=11111, logfile=r'/home/paintball/paintball2/pball/qconsole11111.log', rcon_password='endless')
		   
#@s.event
#def on_chat(nick, message):
#    if message == '!rank':
#        open ranking_list file
#		    read ranking_list for top3_weekly
#	        read ranking_list for nick
#		        if nick exists
#			        add point to nick
#			    else
#			        do nothing

#@s.event		
#def on_chat(nick, message):
#    if message == '!Overall':
#        open ranking_list file
#		    read ranking_list for top3_overall
#	        read ranking_list for nick
#		        if nick exists
#			        add point to nick
#			    else
#			        do nothing

#@s.event
#def on_flag_captured(team, nick, flag):
#    open ranking_list file
#	    read ranking_list for nick
#		    if nick exists
#			   add point to nick
#			else
#			    do nothing

#@s.event
#def on_mapchange(mapname):
#    open ranking_list
#	    seek for most points #1 #2 #3
#		    define rankings nick1, nick2, nick3
#		        s.say('Current Rankings: #1{}, #2{}, #3{}'.format(nick1, nick2, nick3))
#    close ranking_list

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    print('Elimination. Killer\'s nick: {0}, Killer\'s weapon: {1}, Victim\'s nick: {2}, Victim\'s weapon: {3}'
        .format(
        killer_nick, killer_weapon, victim_nick, victim_weapon
    ))
    while i < len(player_list):
        if killer_nick in player_list[i].player.name:
	        player.add_score(1)

@s.event
def on_entrance(nick, build, addr):
    print('Entrance. Nick: {0}, Build: {1}, Address: {2}'.format(nick, build, addr))
    check_if_player_exists (nick)
	
#TEST
player_list = []
top_three = [('player1', 0), ('player2', 0), ('player3', 0), ]

def get_top_three():
    while i < len(player_list):
       if  player_list[i].player.score > top_three[0]:
           del top_three[0]
           top_three[0] = [player.name, player.score]
       if  player_list[i].player.score > top_three[1]:
           del top_three[1]
           top_three[1] = [player.name, player.score]
       if  player_list[i].player.score > top_three[2]:
           del top_three[2]
           top_three[2] = [player.name, player.score]

def check_if_player_exists(nick):
    while i < len(player_list):
        if nick in player_list[i].player.name:
            print('Player: " + player + "already in list.')
            s.say('player.name + " " +player.score')
            return

    print('Player: " + player + "added to list.')
    add_player(player)
    s.say('player.name +" " +player.score')
def add_player(player):
	player_list.append(player)
		
def init_player(name, score):
    player = Player(name, score)
    
class Player():
    name = ""
    score = ""
	
    def init(self, name, score):
	    self.name = name
	    self.score = score
		
    def add_score(new_score):
	    score = score + new_score

s.run()
