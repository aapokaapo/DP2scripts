# Copyright (C) 2022  Aapo Kinnunen
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

from asyncio import sleep
from dplib.server import Server
import sqlite3


print("ServerSide DP2stat running. Made by whoa (and Toolwut)\n------- making Digital Paintball2 great again! -------")

# Create a database if it doesn't already exist
try:
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE players (
    player_id INTEGER PRIMARY KEY NOT NULL, 
    nick TEXT UNIQUE,
    discord_id INTEGER UNIQUE,
    dplogin INTEGER UNIQUE DEFAULT NULL
    );  
    
    CREATE TABLE matches (
    match_id INTEGER NOT NULL PRIMARY KEY,
    date TEXT DEFAULT current_timestamp,
    map TEXT,
    gamemode TEXT,
    result TEXT,
    playtime FLOAT
    );
    
    CREATE TABLE player_performances (
    performance_id INTEGER NOT NULL PRIMARY KEY,
    match_id INTEGER NOT NULL,  
    player_id INTEGER NOT NULL,
    date TEXT DEFAULT current_timestamp,
    nick TEXT,
    dplogin INTEGER,
    kills INTEGER DEFAULT '0',
    deaths INTEGER DEFAULT '0',
    grabs INTEGER DEFAULT '0',
    caps INTEGER DEFAULT '0',
    pgp_shots INTEGER DEFAULT '0',
    pgp_kills INTEGER DEFAULT '0',
    pgp_accuracy FLOAT DEFAULT '0.0',
    trracer_shots INTEGER DEFAULT '0',
    trracer_kills INTEGER DEFAULT '0',
    trracer_accuracy FLOAT DEFAULT '0.0',
    stingray_shots INTEGER DEFAULT '0',
    stingray_kills INTEGER DEFAULT '0',
    stingray_accuracy FLOAT DEFAULT '0.0',
    vm_68_shots INTEGER DEFAULT '0',
    vm_68_kills INTEGER DEFAULT '0',
    vm_68_accuracy FLOAT DEFAULT '0.0',
    spyder_se_shots INTEGER DEFAULT '0',
    spyder_se_kills INTEGER DEFAULT '0',
    spyder_se_accuracy FLOAT DEFAULT '0.0',
    carbine_shots INTEGER DEFAULT '0',
    carbine_kills INTEGER DEFAULT '0',
    carbine_accuracy FLOAT DEFAULT '0.0',
    autococker_shots INTEGER DEFAULT '0',
    autococker_kills INTEGER DEFAULT '0',
    autococker_accuracy FLOAT DEFAULT '0.0',
    automag_shots INTEGER DEFAULT '0',
    automag_kills INTEGER DEFAULT '0',
    automag_accuracy FLOAT DEFAULT '0.0',
    paintgren_thrown INTEGER DEFAULT '0',
    paintgren_kills INTEGER DEFAULT '0',
    paintgren_accuracy FLOAT DEFAULT '0.0',
    kills_to_shots TEXT DEFAULT '0/0',
    total_accuracy TEXT DEFAULT '0.00%',
    total_time_alive FLOAT DEFAULT '0.0',
    total_time_elim FLOAT DEFAULT '0.0',
    shots_to_sec FLOAT DEFAULT '0.0',   
    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
    );
    
    """)
    con.close()
    print("DataBase Created succesfully")
except sqlite3.OperationalError as e:
    print("DataBase already exists")
    print(e)


# Configure server to listen to
s = Server(hostname='localhost', port=27910,
           logfile=r'C:/Games/Paintball2/pball/qconsole27910.log',
           rcon_password='hackme')

round_started = False

@s.event
def on_round_started():
    """
    Declare round started

    :return:
    """
    global round_started
    round_started = True


@s.event
def on_round_end():
    """
    Declare round end

    :return:
    """
    global round_started
    round_started = False


@s.event
def on_chat(nick, message):
    """
    Listen for commands and respond to them

    :param nick:
    :param message:
    :return:
    """
    if message == '!stats':
        pass

    if message == '!top10':
        pass

    if message == '!top10kd':
        pass

    if message == '!help':
        pass


@s.event
def on_namechange(old_nick, new_nick):
    """
    Declare name change

    :param old_nick:
    :param new_nick:
    :return:
    """
    if not old_nick == "":
        sleep(1)
        players = s.get_players()
        for player in players:
            if player.nick == new_nick and player.dplogin != "bot":
                print("Name change: {} -> {} {}  ".format(old_nick, new_nick, player.dplogin))
                if player.dplogin == '':
                    player.dplogin = None
                try:
                    con = sqlite3.connect('stats.db')
                    cur = con.cursor()
                    cur.execute(
                        """
                        UPDATE players 
                        SET 
                        nick = ?,
                        dplogin = ?
                        WHERE nick = ?
                        """, (player.nick, player.dplogin, old_nick)
                    )
                    con.commit()
                    print("Change succesfully logged")
                    con.close()
                except sqlite3.IntegrityError as e:
                    print(e)



@s.event
def on_entrance(nick, build, addr):
    """
    Declare entrance

    :param nick: Nickname of the player who entered
    :param build: Client build number
    :param addr: Client IP address
    :return:
    """
    sleep(1)
    players = s.get_players()
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    for player in players:
        if player.nick == nick and player.dplogin != "bot":
            if player.dplogin == '':
                player.dplogin = None
            try:

                cur.execute(
                    """
                    INSERT INTO players(
                        nick,
                        dplogin
                    ) 
                    VALUES (
                    ?,
                    ?
                    );                    
                    """, (player.nick, player.dplogin)
                )
                con.commit()
                print(player.nick + " added to database with dplogin: " + str(player.dplogin))
            except sqlite3.IntegrityError:
                print(player.nick + " already in database")
                if player.dplogin != "":
                    con = sqlite3.connect('stats.db')
                    cur = con.cursor()
                    cur.execute(
                        """
                        UPDATE players 
                        SET nick = ?,
                            dplogin = ? 
                        WHERE (
                            dplogin = ?
                            OR
                            nick = ?
                        )
                        """, (player.nick, player.dplogin, player.dplogin, player.nick))
                    con.commit()
            try:
                cur.execute(
                    """
                    INSERT INTO player_performances(
                        match_id, 
                        player_id, 
                        nick, 
                        dplogin
                    )
                    VALUES(
                        (SELECT MAX(match_id) FROM matches), 
                        (SELECT player_id FROM players WHERE nick = ?), 
                        ?, 
                        ?
                    );                    
                    """, (player.nick, player.nick, player.dplogin)
                )
                con.commit()
            except sqlite3.IntegrityError as e:
                print(e)
    cur.close()
    con.close()


@s.event
def on_flag_captured(team, nick, flag):
    """
    Add one point to 'Captures'

    :param team: Scoring team color
    :param nick: Scoring player
    :param flag: Scored flag color
    :return:
    """
    if round_started:
        sleep(1)
        players = s.get_players()
        for player in players:
            if player.nick == nick:
                con = sqlite3.connect('stats.db')
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE player_performances 
                    SET caps = caps + 1 
                    WHERE performance_id = (SELECT performance_id 
                                            FROM player_performances 
                                            WHERE player_id = (SELECT player_id 
                                                               FROM players 
                                                               WHERE nick=?) 
                                                               ORDER BY performance_id DESC 
                                                               LIMIT 1)
                    """, (player.nick,))
                con.commit()
                con.close()


@s.event
def on_flag_grab(nick, flag):
    """
    Add one point to 'Captures'

    :param team: Scoring team color
    :param nick: Scoring player
    :param flag: Scored flag color
    :return:
    """
    if round_started:
        sleep(1)
        players = s.get_players()
        for player in players:
            if player.nick == nick:
                con = sqlite3.connect('stats.db')
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE player_performances 
                    SET grabs = grabs + 1 
                    WHERE performance_id = (SELECT performance_id 
                        FROM player_performances 
                        WHERE player_id = (SELECT player_id 
                                           FROM players 
                                           WHERE nick=?) 
                                           ORDER BY performance_id DESC 
                                           LIMIT 1)
                    """, (player.nick,))
                con.commit()
                con.close()


@s.event
def on_elim_teams_flag(team, nick, points):
    """
    Add one point to 'Grabs'

    :param team: Scoring team color
    :param nick: Scoring player
    :param points: Awarded points
    :return:
    """


@s.event
def on_elim(killer_nick, killer_weapon, victim_nick, victim_weapon, suicide):
    """
    Add one point to kills for killer and one point to deaths for victim

    :param killer_nick: Player who got a kill
    :param killer_weapon:
    :param victim_nick: Player who got killed
    :param victim_weapon:
    :param: suicide: Declares whether the kill was a suicide
    :return:
    """
    if round_started:
        con = sqlite3.connect('stats.db')
        cur = con.cursor()
        cur.execute(
            """
            UPDATE player_performances SET kills = kills + 1 
            WHERE performance_id = (SELECT performance_id 
                        FROM player_performances 
                        WHERE player_id = (SELECT player_id 
                                           FROM players 
                                           WHERE nick=?) 
                                           ORDER BY performance_id DESC 
                                           LIMIT 1)
            """, (killer_nick,))
        con.commit()

        cur.execute(
            """
            UPDATE player_performances SET deaths = deaths + 1 
            WHERE performance_id = (SELECT performance_id 
                        FROM player_performances 
                        WHERE player_id = (SELECT player_id 
                                           FROM players 
                                           WHERE nick=?) 
                                           ORDER BY performance_id DESC 
                                           LIMIT 1)
            """, (victim_nick,))
        con.commit()
        if suicide:
            cur.execute(
                """
                UPDATE player_performances SET deaths = deaths + 1 
                WHERE performance_id = (SELECT performance_id 
                        FROM player_performances 
                        WHERE player_id = (SELECT player_id 
                                           FROM players 
                                           WHERE nick=?) 
                                           ORDER BY performance_id DESC 
                                           LIMIT 1)
                """, (killer_nick,))
            con.commit()
        con.close()


@s.event
def on_mapchange(mapname):
    """
    Declare map change

    :param mapname:
    :return:
    """
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO matches(map) VALUES ?
        """, (mapname,)
    )
    con.commit()
    con.close()


@s.event
def gamemode(gamemode):
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.execute(
        """
        UPDATE matches 
        SET gamemode = ?
        WHERE match_id = (SELECT MAX(match_id) FROM matches)
        """, (gamemode,)
    )
    con.commit()
    con.close()



@s.event
def on_game_end(time, results):
    """

    :param results:
    :param time:
    :return:
    """
    print("Game has ended")
    global round_started
    round_started = False
    print(results + " Time:" + time)
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.execute(
        """
        UPDATE matches 
        SET result = ? 
        WHERE match_id = (SELECT MAX(match_id) FROM matches);
        
        UPDATE matches 
        SET playtime = ? 
        WHERE match_id = (SELECT MAX(match_id) FROM matches);
        """, (results, time)
    )
    con.commit()
    con.close()


@s.event
def log_stats(nick, pgp_shots, pgp_kills, pgp_accuracy, trracer_shots, trracer_kills, trracer_accuracy, stingray_shots, stingray_kills, stingray_accuracy, vm_68_shots, vm_68_kills, vm_68_accuracy, spyder_se_shots, spyder_se_kills, spyder_se_accuracy, carbine_shots, carbine_kills, carbine_accuracy, autococker_shots, autococker_kills, autococker_accuracy, automag_shots, automag_kills, automag_accuracy, paintgren_thrown, paintgren_kills, paintgren_accuracy, kills_to_shots, total_accuracy, total_time_alive, total_time_elim, shots_to_sec):
    print("Logging stats for: " + nick)
    con = sqlite3.connect('stats.db')
    cur = con.cursor()
    cur.execute(
        """
        UPDATE player_performances
        SET
            pgp_shots = ?,
            pgp_kills = ?,
            pgp_accuracy = ?,
            trracer_shots = ?,
            trracer_kills = ?,
            trracer_accuracy = ?,
            stingray_shots = ?,
            stingray_kills = ?,
            stingray_accuracy = ?,
            vm_68_shots = ?,
            vm_68_kills = ?,
            vm_68_accuracy = ?,
            spyder_se_shots = ?,
            spyder_se_kills = ?,
            spyder_se_accuracy = ?,
            carbine_shots = ?,
            carbine_kills = ?,
            carbine_accuracy = ?,
            autococker_shots = ?,
            autococker_kills = ?,
            autococker_accuracy = ?,
            automag_shots = ?,
            automag_kills = ?,
            automag_accuracy = ?,
            paintgren_thrown = ?,
            paintgren_kills = ?,
            paintgren_accuracy = ?,
            kills_to_shots = ?,
            total_accuracy = ?,
            total_time_alive = ?,
            total_time_elim = ?,
            shots_to_sec = ?
        
        WHERE performance_id = (SELECT performance_id FROM player_performances WHERE player_id = (SELECT player_id FROM players WHERE nick=?) ORDER BY performance_id DESC LIMIT 1)
        """, (
                pgp_shots,
                pgp_kills,
                pgp_accuracy,
                trracer_shots,
                trracer_kills,
                trracer_accuracy,
                stingray_shots,
                stingray_kills,
                stingray_accuracy,
                vm_68_shots,
                vm_68_kills,
                vm_68_accuracy,
                spyder_se_shots,
                spyder_se_kills,
                spyder_se_accuracy,
                carbine_shots,
                carbine_kills,
                carbine_accuracy,
                autococker_shots,
                autococker_kills,
                autococker_accuracy,
                automag_shots,
                automag_kills,
                automag_accuracy,
                paintgren_thrown,
                paintgren_kills,
                paintgren_accuracy,
                kills_to_shots,
                total_accuracy,
                total_time_alive,
                total_time_elim,
                shots_to_sec,
                nick
            )
    )
    con.commit()
    con.close()


s.run(scan_old=True)


