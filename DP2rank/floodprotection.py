from playerstats import PlayerStats 
import config

s = config.s

on_timeout = []
on_timeout_kd = []

def floodprotection(nick):
    players = s.get_players()
    player_found = False
    for player in players:
        if nick == player.nick:
            the_player = player
    for player in on_timeout:
        if the_player.dplogin == player.id:
            player_found = True
            print("this should stop flooding")
            flooding = True
            return flooding
            break
    if not player_found:
        on_timeout.append(PlayerStats(the_player.nick, the_player.dplogin))

def floodprotection_kd(nick):
    players = s.get_players()
    player_found = False
    for player in players:
        if nick == player.nick:
            the_player = player
    for player in on_timeout_kd:
        if the_player.dplogin == player.id:
            player_found = True
            print("this should stop flooding")
            flooding = True
            return flooding
            break
    if not player_found:
        on_timeout_kd.append(PlayerStats(the_player.nick, the_player.dplogin))