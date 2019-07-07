from dplib.server import Server


s = Server(hostname='127.0.0.1', port=27910,
           logfile=r'C:/Games/Paintball2/pball/qconsole27910.log',
           rcon_password='whoaisbest')

version = str(1.0)
savefile = "server-stats" + version + ".log"