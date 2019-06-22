from dplib.server import Server
import random
from time import sleep
import asyncio

# ***config***

s = Server(hostname='127.0.0.1', port=33333,
           logfile=r'/home/paintball/paintball2/pball/qconsole33333.log',
           rcon_password='hackme')

# you can add silly names for the bots here
# separate names with comma ","
# name_list = ["whoa", "Toolwut"]
name_list = []

# how many bots to add when player joins
bot_count = 10

# ***config ends***


active_players = []


class PlayerInfo():
    def __init__(self, nick, id):
        self.nick = nick
        self.id = id


def load_names():
    try:
        with open("/var/www/html/whoa.ga/leaderboard.txt", "r") as myfile:
            name_list.clear()
            for line in myfile:
                if not line.startswith("#"):
                    saved_player = line.split()
                    nick = saved_player[7]
                    name_list.append(nick)
    except FileNotFoundError:
        print("no name list found")


load_names()

print("whoa's bot script running! version 0.2\nPress Ctrl+C to stop")


def get_teams():
    status = s.get_status()
    scores = status.get("_scores")
    colors = scores.split()
    if colors[0].startswith("Red"):
        team1 = "red"
    elif colors[0].startswith("Yellow"):
        team1 = "yellow"
    elif colors[0].startswith("Purple"):
        team1 = "purple"
    elif colors[0].startswith("Blue"):
        team1 = "blue"
    if colors[1].startswith("Red"):
        team2 = "red"
    elif colors[1].startswith("Yellow"):
        team2 = "yellow"
    elif colors[1].startswith("Purple"):
        team2 = "purple"
    elif colors[1].startswith("Blue"):
        team2 = "blue"
    teams = [team1, team2]
    return teams


def forcejoin_player(nick):
    players = s.get_players()
    for player in players:
        if nick == player.nick:
            entered_player = player
    team = get_teams()
    s.rcon("sv forcejoin " + entered_player.id + " " + team[1])
    player_found = False
    for profile in active_players:
        if profile.id == entered_player.id:
            player_found = True
    if not player_found:
        active_players.append(PlayerInfo(entered_player.nick, entered_player.id))


def add_bots():
    i = 0
    team = get_teams()
    print(str(bot_count) + " bots will be added on team " + team[0])
    for i in range(bot_count):
        bot_name = random.choice(name_list) + "_bot"
        s.rcon("sv addbot " + bot_name)
        i += 1
    players = s.get_players()
    for player in players:
        if player.dplogin == "bot":
            bot = player
            s.rcon("sv forcejoin " + bot.id + " " + team[0])
    print("bots added")


def remove_bots():
    print("Removing " + str(bot_count) + " bots")
    players = s.get_players()
    i = 0
    for player in players:
        if player.dplogin == "bot":
            bot = player
            if i < (bot_count + 1):
                s.rcon("sv removebot " + bot.nick)
                sleep(0.03)
                i += 1


@s.event
def on_team_switched(nick, old_team, new_team):
    teams = get_teams()
    players = s.get_players()
    if teams[1] == "red":
        team = "Red"
    elif teams[1] == "blue":
        team = "Blue"
    elif teams[1] == "yellow":
        team = "Yellow"
    elif teams[1] == "purple":
        team = "Purple"
    if teams[0] == "red":
        bot_team = "Red"
    elif teams[0] == "blue":
        bot_team = "Blue"
    elif teams[0] == "yellow":
        bot_team = "Yellow"
    elif teams[0] == "purple":
        bot_team = "Purple"
    if new_team == "Observer":
        for player in players:
            if player.nick == nick:
                entered_player = player
                player_found = False
                for profile in active_players:
                    if profile.id == entered_player.id:
                        print(nick + " joined observer")
                        active_players.remove(profile)
                        remove_bots()
                        player_found = True
                if not player_found:
                    print(nick + " joined the game")
    if old_team == "Observer":
        print(nick + " came back from observer")
        forcejoin_player(nick)
        print(nick + " joined team " + teams[1])
        add_bots()
    if new_team == bot_team:
        forcejoin_player(nick)


@s.event
def on_disconnect(nick):
    print(nick + " disconnected")
    for player in active_players:
        if player.nick == nick:
            active_players.remove(player)
            remove_bots()


@s.event
def on_game_end(score_blue, score_red, score_yellow, score_purple):
    print("Game ended! Removing bots")
    players = s.get_players()
    for player in players:
        if player.dplogin == "bot":
            bot = player
            sleep(0.03)
            s.rcon("sv removebot " + bot.nick)


@s.event
def on_mapchange(mapname):
    print("Mapchanged! Removing bots")
    players = s.get_players()
    for player in players:
        if player.dplogin == "bot":
            bot = player
            s.rcon("sv removebot " + bot.nick)
    active_players.clear()


@s.event
def on_namechange(old_nick, new_nick):
    players = s.get_players()
    if not old_nick == "":
        if not old_nick.endswith("_bot"):
            asyncio.sleep(1)
            for player in players:
                if player.nick == old_nick:
                    entered_player = player
                    player_found = False
                    for profile in active_players:
                        if profile.id == entered_player.id:
                            profile.nick = new_nick


@s.event
def on_chat(nick, message):
    if message == "!load names":
        load_names()

    elif message == "!debug1":
        print(active_players)


s.run()