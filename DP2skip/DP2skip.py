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
import asyncio
import config
import os
import main

main.cls()

s = config.s

s.rcon("sv_consolename 1")

voting_allowed = False


@s.event
async def on_entrance(nick, build, addr):
    global voting_allowed
    if not voting_allowed:
        await asyncio.sleep(config.timeout)
        voting_allowed = True
    sleep(1)
    main.cls()


@s.event
def on_mapchange(mapname):
    main.clear_lists()
    main.cls()
    global voting_allowed
    voting_allowed = False


@s.event
def on_namechange(old_nick, new_nick):
    for player in main.votenumber:
        if player.name == old_nick:
            player.name = new_nick


@s.event
def on_disconnect(nick):
    print(nick + " disconnected")
    main.remove_vote(nick)
    main.cls()


@s.event
def on_chat(nick, message):
    if message == '!skip':
        if voting_allowed:
            main.vote(nick)
        else:
            s.say(config.text2)


s.run()