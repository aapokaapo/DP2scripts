from config import s, savefile, version
import asyncio
import time
import os

status = s.get_status()
stats = []
player_list = []
players_on_server = ["DPBot01"]
map_time_start = time.time()
map = status["mapname"]


print("Server statistics script running!")

if os.path.exists(savefile):
    pass
else:
    with open(savefile, "w") as myfile:
        myfile.write("#Server stats logger "+ version +
                     "\n#This is the server statistics log file used to track play times and player count on different maps" +
                     "\n#Layout is following:\n#\n#mapname map_playtime\n#nick dplogin time_on_team time_total\n#.\n#.\n#.\n")


class Player:
    def __init__(self,
                 nick,
                 dplogin=None,
                 is_on_team=False,
                 time_start=0.0,
                 time_end=0.0,
                 time_team_start=0.0,
                 time_team_end=0.0,
                 time_team_total=0.0
                 ):

        self.nick = nick
        self.dplogin = dplogin
        self.is_on_team = is_on_team
        self.time_start = time_start
        self.time_end = time_end
        self.time_team_start = time_team_start
        self.time_team_end = time_team_end
        self.time_team_total = time_team_total


def save_stats(map_time_total):
    print("stats save")
    with open(savefile, "a") as myfile:
        myfile.write("\n\n{0} {1}".format(map, int(map_time_total)))
        for player in player_list:
            if player.dplogin == "":
                dplogin = 0
            else:
                dplogin = player.dplogin
            myfile.write(
                "\n{0} {1} {2} {3}".format(player.nick,
                                           dplogin,
                                           int(player.time_team_total),
                                           int(player.time_end - player.time_start))
                )


@s.event
async def on_mapchange(mapname):
    print("map change")
    global map_time_start
    global map
    map_time_end = time.time()
    map_time_total = map_time_end - map_time_start
    map_time_start = time.time()
    for player in player_list:
        player.time_end = map_time_end
        if player.is_on_team:
            player.time_team_end = map_time_end
            player.time_team_total += player.time_team_end - player.time_team_start
    save_stats(map_time_total)
    map = mapname
    player_list.clear()
    players_on_server.clear()


@s.event
async def on_entrance(nick, build, addr):
    print("entrance")
    await asyncio.sleep(1)
    entered_player = None
    player_found = False
    players = s.get_players()
    try:
        for player in players:
            if player.nick == nick:
                if not player.dplogin == "bot":
                    entered_player = player
        for player in player_list:
            if player.dplogin == entered_player.dplogin or player.nick == entered_player.nick:
                player_found = True
        if not player_found:
            player_list.append(Player(entered_player.nick, entered_player.dplogin, time_start=time.time()))
    except AttributeError:
        pass


@s.event
async def on_namechange(old_nick, new_nick):
    if not old_nick == "":
        print("name change")
        for player in player_list:
            if player.nick == old_nick:
                player.nick = new_nick
        for player in players_on_server:
            if player == old_nick:
                players_on_server.remove(old_nick)
                players_on_server.append(new_nick)


@s.event
async def on_team_switched(nick, old_team, new_team):
    if not new_team == "Observer":
        for player in player_list:
            if player.nick == nick:
                player.time_team_start = time.time()
                player.is_on_team = True
    else:
        player_found = False
        for player_name in players_on_server:
            if player_name == nick:
                player_found = True
                for player in player_list:
                    if player.nick == nick:
                        player.time_team_end = time.time()
                        player.is_on_team = False
                        player.time_team_total += player.time_team_end - player.time_team_start
        if not player_found:
            players_on_server.append(nick)


@s.event
async def on_disconnect(nick):
    print("disconnection")
    time_end = time.time()
    for player in player_list:
        if player.nick == nick:
            player.time_end = time_end
            if player.is_on_team:
                player.time_team_end = time_end
                player.time_team_total += player.time_team_end - player.time_team_start
                player.is_on_team = False
    try:
        players_on_server.remove(nick)
    except ValueError:
        pass


s.run()
