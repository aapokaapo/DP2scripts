import discord
import threading
from dplib.server import Server

s = Server(hostname='127.0.0.1', port=xxxx,
           logfile=r'/path/to/logfile/qconsolexxxx.log',
           rcon_password='your_rcon_password_here')

TOKEN = 'discord_bot_token'

client = discord.Client()
channel = ""

@client.event
async def on_message(message):
    if message.author == client.user:
        pass
    elif message.channel != client.get_channel(your_desired_channel_id):
        pass
    else:
        nick = message.author.display_name
        channel = client.get_channel(your_desired_channel)
        msg = message.content
        data = str(nick)+": "+str(msg)
        s.say(data)
        await message.channel.purge(limit=1)
        await channel.send('```diff\n+ {0}: {1}```'.format(nick, msg))
def run_server():
    s.run()
@s.event
async def on_chat(nick, message):
    channel = client.get_channel(your_desired_channel_id)
    await channel.send('```fix\n= {0}: {1} ```'.format(nick, message))
@s.event
async def on_entrance(nick, build, addr):
    channel = client.get_channel(your_desired_channel_id)
    await channel.send('```md\n# {0} entered the game. ```'.format(nick))
@s.event
async def on_mapchange(mapname):
    channel = client.get_channel(your_desired_channel_id)
    await channel.send('```md\n# Map has changed to {0}. ```'.format(mapname))
@s.event
async def on_disconnect(nick):
    channel = client.get_channel(your_desired_channel_id)
    await channel.send('```diff\n- {0} disconnected. ```'.format(nick))
@client.event
async def on_ready():
    print('Success. Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
x = threading.Thread(target=run_server)
x.start()
client.run(TOKEN)
