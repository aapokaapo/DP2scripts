#Config file for DP2skip
from dplib.server import Server

# Define the portnumber, logfile and rcon_password
s = Server(hostname='127.0.0.1', port=11111,
           logfile=r'/home/paintball/paintball2/pball/qconsole11111.log',
           rcon_password='whoaisbest')

# Define the path to server map rotation
rotation = "/home/paintball/paintball2/pball/configs/rotation_test.txt"

# Define the length of timeout, before a new vote can be called
timeout = 10

#Define the messages to be said in the game
# Use "{C}#text" where '#' is a number or letter for colors
# Use "{I}text{/I}" for italic text
# Use "{U}text{/U}" for underlined text

# When first player says '!skip'
# e.g "Vote to skip map requested! To vote yes type '!skip'"
text1="{C}0***{C}DVote to skip map requested! To vote yes type {C}?'!skip'{C}0***"

# When map has just changed
# e.g "Wait few seconds before a new vote"
text2="{C}0***{C}DWait few seconds before a new vote{C}0***"

# When player votes to skip
# e.g "Votes still needed to skip: 2"
text3="{C}0***{C}DVotes still needed to skip:{C}O"

# When player has already voted
# e.g "whoa has already voted yes!"
# text4 defines the prefix and color for the player name
# text5 defines the ending
text4="{C}0***{C}D"
text5="already voted yes!{C}0***"

# This is the timer for mapchange
# e.g "Skip vote passed! Map will be changed in 3"
#     "Map will be changed in 2"
#     "Map will be changed in 1"
text6="{C}0***{C}DSkip vote passed! Map will be changed! in 3{C}0***"
text7="{C}0***{C}DMap will be changed in 2{C}0***"
text8="{C}0***{C}DMap will be changed in 1{C}0***"
