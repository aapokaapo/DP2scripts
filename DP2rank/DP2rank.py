from config import s
from config import infomessage
import main
import threading
    
print("ServerSide DP2RankingSystem running. Made by whoa (and Toolwut)\nClan [s] making Digital Paintball2 great again!")

main.leaderboard_load()



@s.event
def on_chat(nick, message):
    if message == '!stats':
        main.get_stats(nick)

    if message == '!top10':
        main.get_top10()

    if message == '!addplayer':
        main.add_player(nick)

    if message == '!top10kd':
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

t = threading.Timer(300.0, infomessage,())
t.start()

s.run()
