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

from operator import attrgetter
from dplib.server import Server
import numpy as np

s = Server(hostname='178.157.90.120', port=33333, logfile=r'/home/paintball/paintball2/pball/qconsole33333.log', rcon_password='endless')

@s.event
def on_game_end(score_blue, score_red, score_yellow, score_purple):
    print('Game ended. Blue:{} Red:{} Yellow:{} Purple:{}'.format(
        score_blue, score_red, score_yellow, score_purple
    ))
	get_topthree
    s.say('Top3/Week: #1{0}, #2{1}, #3{2}'.format(top1, top2, top3)) 
@s.event
def on_chat(nick, message):
    if message == '!rank':
	    for Player in player_object_list:
		    if nick == Player.name:
			    print('Player ' + nick + ' requested list.')
			    print(str(player_object_list))

			    s.say('{0}: {1}'.format(Player.name, Player.score))

@s.event
def on_flag_captured(team, nick, flag):
    print('Flag captured. Team: {0}, Nick: {1}, Flag: {2}'.format(team, nick, flag))
    for Player in player_object_list:
	    if nick == Player.name:
		    add_score(1)
		    print('Player ' + nick + ' got point!')		    
		    break

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    for Player in player_object_list:
	    if killer_nick == Player.name:
		    Player.add_score(1)
		    break
		    print('Player ' +killer_nick + ' got point!')
@s.event
def on_entrance(nick, build, addr):
    print('Entrance. Nick: {0}, Build: {1}, Address: {2}'.format(nick, build, addr))
    check_if_player_exists(nick)
	
player_object_list = []

def check_if_player_exists(nick):
    print(nick)
    print(str(player_object_list))
    for Player in player_object_list:
	    if nick == Player.name:
		    print('Player ' + nick + ' already on list.')
		    print(str(player_object_list))

		    s.say('{0}: {1}'.format(Player.name, Player.score))
		    break
    else:
	    add_player(nick)
	    print('Player ' +  nick + ' added to list.')
	    print(str(player_object_list))
#def add_player toimii
def add_player(nick):
    player_object_list.append(Player(nick, 0))


class Player():
    name = ""
    score = ""
	
    def __init__(self, name, score):
	    self.name = name
	    self.score = score
		
def add_score(new_score):
    Player.score = Player.score + new_score
	    
def get_topthree(top1, top2, top3):
    

s.run()
