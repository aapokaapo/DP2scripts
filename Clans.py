# DPLib - Asynchronous bot framework for Digital Paint: Paintball 2 servers
# Copyright (C) 2017  MichaÅ‚ Rokita
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
#
# Ranking system

from dplib.server import Server
from dplib.dplogin import DPLogin

s = Server(hostname='127.0.0.1', port=22222,
           logfile=r'/home/paintball/paintball2/pball/qconsole22222.log',
           rcon_password='hackme')

d = DPLogin()


def get_clan(clanid):
    members = d.get_clan_members(clanid)
    print(members)
    for i in range(len(members.get("Leaders"))):
        active_player = members.get("Leaders")[i].get("name")
        active_player_id = members.get("Leaders")[i].get("id")
        s.say(active_player + ":" + active_player_id)

@s.event
def on_chat(nick, message):
    print(nick, message)
    if message.startswith('!getclan'):
        clanid = message.replace("!getclan ","")
        print(nick +" added clanid:" +clanid)
        get_clan(clanid)

        
s.run()
