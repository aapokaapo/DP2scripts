import socket
from playerstats import PlayerStats

savefile = "globalleaderboard.txt"

HOST = '127.0.0.1'
PORT = 50000

ip_whitelist = ["127.0.0.1"]
    
player_list = []
global_player_list = []


def add_points(myfile):
    for line in myfile:
        if not line.startswith("#"):
            saved_player = line.split()
            player_found = False
            for player in global_player_list:
                if player.id == saved_player[6]:
                    player.kills += int(saved_player[2])
                    player.deaths += int(saved_player[3])
                    player.caps += int(saved_player[4])
                    player.grabs += int(saved_player[5])
                    player_found = True
                    break
            if not player_found:
                nick = saved_player[7]
                kills = int(saved_player[2])
                deaths = int(saved_player[3])
                caps = int(saved_player[4])
                grabs = int(saved_player[5])
                id = saved_player[6]
                global_player_list.append(PlayerStats(nick, id, kills, deaths, caps, grabs))
                print(nick + ":" + id)

def global_leaderboard():
    for i in range(len(ip_whitelist))
        whitelisted_ip = ip_whitelist[i]
    with open(whitelisted_ip + "leaderboard.txt", "r") as myfile:
        add_points(myfile)
    
        
def save_global_leaderboard():
    global_player_list.clear()
    global_leaderboard()
    with open(savefile, 'w') as myfile:
        myfile.write("# DP2RankingSystem Global Leaderboard\n# RANK K/D K D C G ID NAME\n")
        print("Global Leaderboard saved.") 
        global_player_list.sort(reverse=True, key=lambda player_stats: player_stats.kills-player_stats.deaths+3*player_stats.grabs+5*player_stats.caps)
        for i in range(len(player_list)):
            player_index = i + 1
            player_stats = player_list[i]
            deaths = player_stats.deaths
            if deaths == 0:
                kd = (float(player_stats.kills)/int(1))
            else:
                kd = (float(player_stats.kills)/float(player_stats.deaths))
            myfile.write(str(player_index) + " "
                + str(kd) + " "
                + str(player_stats.kills) + " "
                + str(player_stats.deaths) + " "
                + str(player_stats.caps) + " "
                + str(player_stats.grabs) + " "
                + str(player_stats.id) + " "
                + player_stats.name + "\n")
                

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ((HOST, PORT))
sock.bind(server_address)
sock.listen(1)
while True:
    connection, client_address = sock.accept()
    for i in range(len(ip_whitelist))
        if not client_address[0] == ip_whitelist[i]:
            connection.close()
            break
    try:
         while True:
            data = connection.recv(1024)
            if data:
                with open(client_address[0] + "leaderboard.txt", "w" ) as myfile:
                    myfile.write(data.decode())
            else:
                break
    

    finally:
        connection.close()  
        save_global_leaderboard()
