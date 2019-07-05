from dplib.server import Server
import random
from time import sleep
import asyncio

s = Server(hostname='127.0.0.1', port=11111,
           logfile=r'/home/paintball/paintball2/pball/qconsole11111.log',
           rcon_password='hackme)

print("whoa's hostage gamemode script running!")
s.rcon("debug3 1;debug1 0;grenadeffire 0;ffire 0;elim 1")

game_started = False
hostage = None
bots = True
player_list = []
guards = []


def get_teams():
    status = s.get_status()
    scores = status.get("_scores")
    team_color = scores.split()
    return team_color


def get_player_list():
    players = s.get_players()
    for player in players:
        if not player.dplogin == "bot":
            player_list.append(player)


def get_hostage():
    global hostage
    get_player_list()
    hostage = random.choice(player_list)
    print("Hostage is: " + hostage.nick)
    player_list.remove(hostage)


def get_guards():
    i = 0
    count = int((len(player_list) + 1) / 2)
    for i in range(count):
        random_player = random.choice(player_list)
        guards.append(random_player.id)
        player_list.remove(random_player)
    print(str(guards))


def add_bots():
    i = 0
    while i < 6:
        s.rcon("sv addbot")
        i += 1


def forcejoin():
    s.rcon("debug3 1")
    if not bots:
        get_guards()
        players = s.get_players()
        for player in players:
            if not player.nick == hostage.nick:
                if not player.id in guards:
                    s.rcon("sv forcejoin " + player.id + " red")
                else:
                    s.rcon("sv forcejoin " + player.id + " blue")
            else:
                s.rcon("sv forcejoin " + player.id + " yellow")
    else:
        players = s.get_players()
        for player in players:
            if not player.nick == hostage.nick:
                if not player.dplogin == "bot":
                    s.rcon("sv forcejoin " + player.id + " red")
                else:
                    s.rcon("sv forcejoin " + player.id + " blue")
            else:
                s.rcon("sv forcejoin " + player.id + " yellow")
    s.rcon("debug3 0")


def game():
    global guards
    guards.clear()
    s.rcon("debug3 1")
    s.rcon("sv forcejoin all o")
    get_hostage()
    forcejoin()
    s.say("Hostage is: " + hostage.nick)


def player_count():
    playernumber = 0
    players = s.get_players()
    for player in players:
        if not player.dplogin == "bot":
            playernumber += 1
    return playernumber


def run_game(nick=None):
    sleep(2)
    players = s.get_players()
    playernumber = player_count()
    global bots
    global game_started
    if not game_started:
        if playernumber > 4:
            s.say("Enough players to play without bots!")
            s.rcon("sv removebot all")
            bots = False
            game_started = True
            game()
        elif playernumber > 1:
            bots = True
            s.say("Not enough players to play without bots!")
            s.say("Adding bots so that the game can start!")
            sleep(1)
            add_bots()
            sleep(1)
            game_started = True
            game()
        else:
            s.say("Need atleast 2 players to play the hostage gamemode")
    else:
        if bots:
            if playernumber > 4:
                s.say("Enough players to play without bots!")
                s.rcon("sv removebot all")
                bots = False
                game()
        else:
            for player in players:
                if player.nick == nick:
                    s.rcon("sv forcejoin " + player.id + " red")


@s.event
def on_entrance(nick, build, addr):
    if not build == 0:
        if not game_started:
            another_player = yield from s.wait_for_entrance(timeout=2)
            if not another_player:
                run_game()
        else:
            run_game(nick)


@s.event
def on_round_started():
    s.rcon("debug3 1")
    s.rcon("sv forcejoin " + hostage.id + " red")
    s.rcon("debug3 0")


@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon, suicide):
    if victim_nick == hostage.nick:
        s.rcon("debug3 1")
        for player in player_list:
            s.rcon("sv forcejoin " + player.id + " o")
        s.say("Hostage died! SWAT lost!")
        sleep(3)
        player_list.clear()
        game()
    if suicide:
        if killer_nick == hostage.nick:
            s.rcon("debug3 1")
            for player in player_list:
                s.rcon("sv forcejoin " + player.id + " o")
            s.say("Hostage couldn't take the pressure! SWAT lost!")
            sleep(3)
            player_list.clear()
            game()


@s.event
def on_flag_captured(team, nick, flag):
    s.say("Hostage freed! SWAT won")
    sleep(3)
    player_list.clear()
    game()


@s.event
def on_mapchange(mapname):
    global round_started
    global bots
    round_started = False
    bots = True
    s.rcon("sv removebot all")


@s.event
def on_team_switched(nick, old_team, new_team):
    if old_team:
        players = s.get_players()
        for player in players:
            if nick == player.nick:
                s.rcon("sv forcejoin " + player.id + " " + old_team)


@s.event
def on_disconnect(nick):
    if nick == hostage.nick:
        s.rcon("debug3 1")
        s.rcon("sv forcejoin all o")
        s.say("Hostage couldn't take it! SWAT lost!")
        sleep(3)
        game()
    else:
        run_game()
    print(nick + " disconnected")


s.run()