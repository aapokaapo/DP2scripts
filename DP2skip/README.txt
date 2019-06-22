### DP2skip script made by Aapo Kinnunen aka. whoa ###

source available at: https://github.com/aapokaapo/DP2skip

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

### What it is and how it works?: ###
- When player says "!skip" he votes to skip map
- If the majority has voted yes, the server will skip the map and change to the next map in rotation
- The script relies heavily on mRokita's DPLib
- The script uses rcon to change the map

### Known bugs: ###
- none, if you find any please inform me.

### Installation: ###

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

3. Configure config.py with a text editor
	- set the path to your server log file
	- set the rcon password for your server
	- set the path to your server's rotation file

4. Run DP2skip.py
	- python DP2skip.py