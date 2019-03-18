from dplib.server import Server
from time import sleep
import threading

# Define the portnumber, logfile and rcon_password
s = Server(hostname='127.0.0.1', port=11111,
           logfile=r'/home/paintball/paintball2/pball/qconsole11111.log',
           rcon_password='hackme')
           
# Define where the script will save the leaderboard
savefile = "leaderboard.txt"

# Define the automated infomessages you want to say on your server
# {C}I where I = color character
# {I}This text will be in italic{I}
# {U}This text will be underlined{U}
infomessage_enabled = True

message1 ="{C}0***{C}DThis server is running Leaderboard(TM){C}0***"

message2 ="{C}0***{C}DTo add yourself to the leaderboard, type !addplayer{C}0***"

message3 ="{C}0***{C}DTo see your stats type !stats{C}0***"

message4 ="{C}0***{C}DType {C}?!help {C}Dfor additional info{C}0***"

def infomessage():
    if infomessage_enabled:
        s.say(message1)
        sleep(0) #time in seconds
        
        s.say(message2)
        sleep(0) #time in seconds
        
        s.say(message3)
        sleep(0) #time in seconds.
        
        s.say(message4)    


