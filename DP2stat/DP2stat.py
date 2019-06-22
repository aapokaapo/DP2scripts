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

from time import sleep
from config import s
from config import infomessage
import main
import threading
import floodprotection as f
import GSclient
import crython
    
print("ServerSide DP2stat running. Made by whoa (and Toolwut)\n------- making Digital Paintball2 great again! -------")

main.leaderboard_load()

round_started = False

@s.event
def on_round_started():
    global round_started
    round_started = True

@s.event
def on_chat(nick, message):
    if message == '!stats':
        flooding = False
        if not flooding:
            main.get_stats(nick)

    if message == '!top10':
        flooding = False
        flooding = f.floodprotection_top10(nick)
        if not flooding:
            main.get_top10()

    if message == '!top10kd':
        flooding = False
        flooding = f.floodprotection_top10kd(nick)
        if not flooding:
            main.get_top10kd()
        
    if message == '!help':
        main.get_help()
        
@s.event
def on_namechange(old_nick, new_nick):
    if not old_nick == "":
        sleep(1)
        main.add_player(new_nick)
     
@s.event
def on_entrance(nick, build, addr):
    sleep(1)
    main.add_player(nick)

@s.event
def on_flag_captured(team, nick, flag):
    if round_started:
        for player_stats in main.player_list:
            if nick == player_stats.name:
                player_stats.add_capture()
                break

@s.event
def on_elim_teams_flag(team, nick, points):
    if round_started:
        for player_stats in main.player_list:
            if nick == player_stats.name:
                player_stats.add_grab()
                break

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    print("elimination")
    if round_started:
        for player_stats in main.player_list:
            if killer_nick == player_stats.name:
                player_stats.add_kill()
            if victim_nick == player_stats.name:
                player_stats.add_death()

@s.event
def on_mapchange(mapname):
    global round_started
    round_started = False
    main.leaderboard_save()
    f.on_timeout_stats.clear()
    f.on_timeout_top10.clear()
    f.on_timeout_top10kd.clear()
#    GSclient.leaderboard_save()

@crython.job(expr='0 0 0 0 1 * *')
def statsboard_reset():
    main.stats_reset()

if __name__ == '__main__':
    crython.tab.start() #start the global cron tab scheduler which runs in a background thread

t = threading.Timer(300.0, infomessage) #this defines how often the automated infomessage runs, time in seconds (default 300)
t.start()

s.run()
