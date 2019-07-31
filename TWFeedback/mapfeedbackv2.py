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
from shutil import copyfile
import os
import time
import threading

s = Server(hostname='127.0.0.1', port=11111,
           logfile=r'/home/paintball/paintball2/pball/qconsole11111.log',
           rcon_password='oAQrge5x')
           
### Unchanged from mapfeedback.py - store feedback in map_name specific file with nick ###
def add_feedback(feedback, nick):
    status = s.get_status()
    mapname=status.get("map_name")
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

def remove_feedback(linenumber, nick):
    status = s.get_status()
    mapname=status.get("map_name")
    try:
        linenumber=int(linenumber)
    except ValueError:
        s.say("Error, please enter a linenumber")
    ### Retrieve player's ID ###
    players=s.get_players()
    playerid = 0
    for player in players:
        if player.nick == nick:
            if not player.dplogin:
                playerid=0
            else:
                playerid=int(player.dplogin)
            break
    ### check if player and mapper have an ID > 0 ###
    if playerid == 0:
        s.say("You must be logged in to your Global Login Account to remove feedback")
        return None
    mapperid = get_mapper(mapname)
    if mapperid == 0:
        return None
    ### remove the line ###
    if playerid == mapperid:
        if mapname.startswith("beta"):
            cleanmapname = mapname.replace("beta/", "")
        elif mapname.startswith("inprogress"):
            cleanmapname = mapname.replace("inprogress/", "")
        remove_line("/var/www/html/whoa.ga/feedback/"+cleanmapname, linenumber)
        s.say("Line removed, refresh your browser to see it at "+"www.whoa.ga/feedback/"+cleanmapname+".txt")
    else:
        s.say("You're not set as the mapper, contact the admins if you want to be")
        
def set_mapper(mapper, nick):
    ### Get nick's ID and check if it's whoa or Toolwut ###
    status=s.get_status()
    mapname=status.get("map_name")
    try:
        mapperid=int(mapper)
    except ValueError:
        s.say("Error, please enter a valid DPLogin ID")
        return None
    players=s.get_players()
    playerid = 0
    for player in players:
        if player.nick == nick:
            if not player.dplogin:
                playerid=0
            else:
                playerid=int(player.dplogin)
            break
    isadmin=False
    if playerid==52566:
        s.say("nice ... its whoa")
        isadmin=True
    elif playerid == 219228:
        s.say("Toolwut <3")
        isadmin=True
    else:
        s.say("youre no admin")
        return None
    ### Check if map_name already has an admin set ###
    mapperfile="/var/www/html/whoa.ga/mapperlist.txt"
    if not os.path.exists(mapperfile):
        s.say("No mapperfile specified")
        return None
    f=open(mapperfile, "r")
    alreadyspecified=False
    for line in f:
        if line.startswith(mapname):
            s.say("mapper for "+mapname+" already specified, overwriting ...")
            alreadyspecified=True
            oldmapper=line.replace(mapperfile+" ","")
            newline=mapper
            replaceline("/var/www/html/whoa.ga/mapperlist", line, mapname+" "+mapper)
            break
    f.close()
    if not alreadyspecified:
        f=open(mapperfile, "a")
        f.write(mapname+" "+mapper+"\n")
        f.close()
        s.say("appended mapper for "+mapname+" to mapperfile")

def replaceline(path, oldcontent, newcontent):
    copyfile(path+".txt", path+"tmp.txt")
    g=open(path+".txt", "w")
    #with os.fdopen(path+".txt", "w") as new_file:
    with open(path+"tmp.txt") as old_file:
        for line in old_file:
            if(line == oldcontent):
                g.write(newcontent)
            else:
                g.write(line)
    g.close()
    os.remove(path+"tmp.txt")

def remove_line(path, linenumber):
    copyfile(path+".txt", path+"tmp.txt")
    g=open(path+".txt", "w")
    whichline=0
    with open(path+"tmp.txt") as old_file:
        for line in old_file:
            whichline += 1
            if not whichline == linenumber:
                g.write(line)
    g.close()
    os.remove(path+"tmp.txt")

def get_mapper(mapname):
    ### Mapper list file ###
    mapperfile="/var/www/html/whoa.ga/mapperlist.txt"
    ### Check if file exists ###
    if not os.path.exists(mapperfile):
        s.say("No mapperfile specified")
        return 0
    ### check if mapperfile lines consist of "<map_name> <mapper-ID>" and return mapper ID ###
    else:
        f=open(mapperfile, "r")
        for line in f:
            if line.startswith(mapname):
                line=line.replace(mapname+" ","")
                try:
                    linenumber=int(line)
                except ValueError:
                    print("Invalid mapperfile content: "+line)
                return linenumber
        s.say("No mapper for this map_name specified, please contact the admin (whoa or Toolwut)")
        return 0

### Receive order to store feedback or to remove feedback ###
@s.event
def on_chat(nick, message):
    if message.startswith('!feedback'):
        add_feedback(message.replace("!feedback ",""), nick)
    elif message.startswith("!removeline"):
        remove_feedback(message.replace("!removeline ",""), nick)
    elif message.startswith("!setmapper"):
        set_mapper(message.replace("!setmapper ",""), nick)

def infomessage():
    s.say("{C}0***{C}Eto give feedback type '!feedback <your feedback here>'{C}0***")  
    s.say("{C}0***{C}ETo the mapper: to remove feedback type '!removeline <linenumber>, make sure to be logged in'{C}0***")  
    t = threading.Timer(300.0, infomessage,())
    t.start()

t = threading.Timer(180.0, infomessage,())
t.start()
    
s.run()
