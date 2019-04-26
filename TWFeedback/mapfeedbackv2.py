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
import os
import time
import threading

s = Server(hostname='127.0.0.1', port=22222,
           logfile=r'/home/paintball/paintball2/pball/qconsole22222.log',
           rcon_password='whoaisbest')
           
           
def add_feedback(feedback, nick):
    status = s.get_status()
    mapname=status.get("mapname")
    if mapname.startswith("beta"):
        mapname = mapname.replace("beta/", "")
    elif mapname.startswith("inprogress"):
        mapname = mapname.replace("inprogress/", "")
    filename = "/var/www/html/whoa.ga/feedback/"+mapname+".txt"

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(filename ,append_write) as myfile:
        myfile.write(nick+": "+feedback + "\n")
        s.say("{C}9***{C}Cfeedback added to whoa.ga/feedback/"+mapname + ".txt{C}9***")
   

@s.event
def on_chat(nick, message):
    if message.startswith('!feedback'):
        add_feedback(message.replace("!feedback",""), nick)

def infomessage():
    s.say("{C}0***{C}Eto give feedback type '!feedback <your feedback here>'{C}0***")  
    t = threading.Timer(300.0, infomessage,())
    t.start()

t = threading.Timer(180.0, infomessage,())
t.start()
    
s.run()