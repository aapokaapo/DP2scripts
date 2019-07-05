DP2stat beta 2 made by whoa

source available at: https://github.com/aapokaapo/DP2scripts/DP2stat

 Copyright (C) 2019  Aapo Kinnunen

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.


Thanks to:

	- mRokita for making the DPLib this script relies heavily on
	- Toolwut for supporting, mentoring and testing this script
	- to the person who is using this on his server

###Installation###

1. You must have Python 3.x installed, if not there are instructions online for this

2. Installing DPLib:
	Install method #1:
	This will install the DPLib to current user's /.local directory
	- cd DPLib
	- python setup.py install --prefix=$HOME/.local

	Install method #2:
	- cd DPLib
	- install pip for python
	- python -m pip install DPLib
	This will overwrite mRokitas server.py with my modified server.py
	- cp dplib/server.py $HOME/.local/lib/python3.*/site-packages/dplib/

2.1 Installing crython:
	Install crython to monthly reset the stats
	- python -m pip intall crython

3.Configure DP2stat config.py
	-set the server port
	-set the path to the servers log file
	-set the rcon password for your server
	-set the path for savefile
	-modify the automated messages to your liking, or disable them

4.Run DP2stat.py
	-use command:
		python3 DP2stat.py

(5.Modify server.cfg)
	- add [s] to your server hostname, so people will know the server is running DP2stat

(6.Monthly reset)
	- edit your crontab schedule


###In-game commands and usage###
Currently there are 5 in-game commands

	1."!addplayer"
		-adds player to the DP2Leaderboard(TM)
		-is bound to players Global Login id, so the player must be logged in
		-if the player changes his nick, he has to add himself again to notify the script of name change

	2."!stats"
		-prints the stats of the user
		-kills|deaths|captures|grabs|score|kills/deaths -ratio

	3."!top10"
		-prints the current top10 players

	4."!top10kd"
		-prints the current top10 base on k/d -ratio

	5."!help"
		-print the commands and their meaning in-game

The script saves the leaderboard automatically and loads it on start-up

###Incoming updates###

1.Global ranking

2.Automated script to notice name changes
