from playerstats import PlayerStats 
import config

s = config.s

on_timeout_stats = []
on_timeout_top10 = []
on_timeout_top10kd = []

def floodprotection_stats(nick):
    players = s.get_players()
    player_found = False
    for player in players:
        if nick == player.nick:
            the_player = player
    for player in on_timeout_stats:
        if the_player.dplogin == player.id:
            player_found = True
            print("this should stop flooding")
            flooding = True
            return flooding
    if not player_found:
        on_timeout_stats.append(PlayerStats(the_player.nick, the_player.dplogin))

def floodprotection_top10(nick):
    players = s.get_players()
    player_found = False
    for player in players:
        if nick == player.nick:
            the_player = player
    for player in on_timeout_top10:
        if the_player.dplogin == player.id:
            player_found = True
            print("this should stop flooding")
            flooding = True
            return flooding
    if not player_found:
        on_timeout_top10.append(PlayerStats(the_player.nick, the_player.dplogin))

def floodprotection_top10kd(nick):
    players = s.get_players()
    player_found = False
    for player in players:
        if nick == player.nick:
            the_player = player
    for player in on_timeout_top10kd:
        if the_player.dplogin == player.id:
            player_found = True
            print("this should stop flooding")
            flooding = True
            return flooding
            break
    if not player_found:
        on_timeout_top10kd.append(PlayerStats(the_player.nick, the_player.dplogin))
