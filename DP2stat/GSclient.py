import socket
from main import player_list
from config import savefile





def leaderboard_save():
    try:
        print("Trying to send leaderboard to master server")
        try:
            #send data
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 50000)
            sock.connect(server_address)
            with open(savefile, "r") as myfile:
                data = myfile.read().encode()
                sock.send(data)
            
        finally:
            sock.close()
    except ConnectionRefusedError:
        print("Connection to master server refused")