from dplib.server import Server
import random
from time import sleep


# ***config***

s = Server(hostname='127.0.0.1', port=27911,
           logfile=r'/home/user/paintball2/pball/qconsole27911.log',
           rcon_password='hackme')

# you can add silly names for the bots here
# separate names with comma ","
# name_list = ["whoa", "Toolwut"]
name_list = ['Colton']

# how many bots to add when player joins
bot_count = 10

# ***config ends***


active_players = []

s.rcon("g_autobalance 0")
s.rcon("debug3 1")
s.rcon("g_autojoin 0")


def load_names():
    try:
        with open("/var/www/html/leaderboard.txt", "r") as myfile:
            name_list.clear()
            for line in myfile:
                if not line.startswith("#"):
                    saved_player = line.split()
                    nick = saved_player[7]
                    name_list.append(nick)
    except FileNotFoundError:
        print("no name list found")


load_names()

print("whoa's bot script running! version 0.3\nPress Ctrl+C to stop")


def get_teams():
    """
    Get the team colors from the status and scores.

    :return: Returns a list of team names (colors)
    """
    scores = s.get_status().get("_scores")
    # Returns something like 'Red:0 Blue:0 '
    colors = scores.split()
    team1 = colors[0].split(":")[0].lower()
    team2 = colors[1].lower().split(":")[0]
    return [team1, team2]


def forcejoin_player(player):
    """
    Forcejoin the player to the human team. If they are not in active players, append them.

    :param player:
    :return:
    """
    teams = get_teams()
    s.rcon("sv forcejoin " +player.id + " " + teams[1])
    if player not in active_players:
        active_players.append(player)


def add_bots():
    """
    Adds i amount of bots

    :return:
    """
    i = 0
    teams = get_teams()
    print(str(bot_count) + " bots will be added on team " + teams[0])
    for i in range(bot_count):
        bot_name = random.choice(name_list) + "_bot"
        s.rcon("sv addbot " + bot_name)
        i += 1
    players = s.get_players()
    for player in players:
        if player.dplogin == "bot":
            bot = player
            s.rcon("sv forcejoin " + bot.id + " " + teams[0])
    print("bots added")


def remove_bots():
    """
    Removes i amount of bots. I noticed that having a slight delay between 'disconnects' doesn't make
    the disconnect sound go BOOOOOM

    :return:
    """
    print("Removing " + str(bot_count) + " bots")
    players = s.get_players()
    i = 0
    for bot in players:
        if bot.dplogin == "bot":
            if i < (bot_count + 1):
                s.rcon("sv removebot " + bot.nick)
                sleep(0.03)
                i += 1


def remove_bots_all():
    """
    Removes all bots

    :return:
    """
    print("Removing all bots")
    s.rcon("sv removebot all")


@s.event
def on_team_switched(nick, old_team, new_team):
    """
    Forcejoin players back to human team if they try to join the bot team and update active player list to
    determine how many bots are needed

    :param nick:
    :param old_team:
    :param new_team:
    :return:
    """
    teams = get_teams()
    players = s.get_players()
    bot_team = teams[0]
    human_team = teams[1]

    for new_player in players:
        if new_player.nick == nick:
            if new_team == "Observer":
                player_found = False
                if new_player in active_players:
                    print(nick + " joined observer")
                    active_players.remove(new_player)
                    remove_bots()
                    player_found = True
                if not player_found:
                    print(nick + " joined the game")

            if old_team == "Observer":
                print(nick + " came back from observer")
                forcejoin_player(new_player)
                print(nick + " joined team " + teams[1])
                add_bots()
            if new_team.lower() == bot_team:
                print(nick + " tried to join the bot team " + teams[0] +
                      ", forcejoin him to the human team " + teams[1])
                forcejoin_player(new_player)


@s.event
def on_disconnect(nick):
    """
    Remove disconnected player from active players

    :param nick:
    :return:
    """
    print(nick + " disconnected")
    for player in active_players:
        if player.nick == nick:
            active_players.remove(player)
            remove_bots()


@s.event
def on_game_end(score_blue, score_red, score_yellow, score_purple):
    """
    Remove bots and clear active players. In other words reset when the map ends.

    :param score_blue:
    :param score_red:
    :param score_yellow:
    :param score_purple:
    :return:
    """
    print("Game ended! Removing bots")
    remove_bots_all()
    active_players.clear()



@s.event
def on_mapchange(mapname):
    """
    Remove bots and clear active players. In other words reset when the map changes.

    :param mapname:
    :return:
    """
    print("Mapchanged! Removing bots")
    remove_bots_all()
    active_players.clear()


@s.event
def on_namechange(old_nick, new_nick):
    pass
    """if not old_nick == ("" or "_bot"):
        asyncio.sleep(1)
        players = s.get_players()
        for player in players:
            if player.nick == old_nick:
                entered_player = player
                for profile in active_players:
                    if profile.id == entered_player.id:
                        profile.nick = new_nick"""


@s.event
def on_chat(nick, message):
    if message == "!load names":
        load_names()

    elif message == "!debug1":
        print(active_players)


s.run(scan_old=True)

