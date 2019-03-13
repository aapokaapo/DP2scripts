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


from config import s
from config import infomessage
import main
import threading
import floodprotection as f
import GRclient
    
print("ServerSide DP2RankingSystem running. Made by whoa (and Toolwut)\n------- Clan [s] making Digital Paintball2 great again!-------")

main.leaderboard_load()



@s.event
def on_chat(nick, message):
    if message == '!stats':
        main.get_stats(nick)

    if message == '!top10':
        flooding = False
        flooding = f.floodprotection(nick)
        if not flooding:
            main.get_top10()

    if message == '!addplayer':
        main.add_player(nick)

    if message == '!top10kd':
        flooding = False
        flooding = f.floodprotection_kd(nick)
        if not flooding:
            main.get_top10kd()
        
    if message == '!help':
        main.get_help()


@s.event
def on_flag_captured(team, nick, flag):
    for player_stats in main.player_list:
        if nick == player_stats.name:
            player_stats.add_capture()
            break

@s.event
def on_elim_teams_flag(team, nick, points):
    for player_stats in main.player_list:
        if nick == player_stats.name:
            player_stats.add_grab()
            break

@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon):
    print("elimination")
    for player_stats in main.player_list:
        if killer_nick == player_stats.name:
            player_stats.add_kill()
        if victim_nick == player_stats.name:
            player_stats.add_death()

@s.event
def on_mapchange(mapname):
    main.leaderboard_save()
    GRclient.leaderboard_save()
    f.on_timeout.clear()
    f.on_timeout_kd.clear()

t = threading.Timer(300.0, infomessage,())
t.start()

s.run()
