# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!", "James, ")
TOKEN = "NTk2NzUxNzQzODAzNzE5Njgw.XR-KJA.AakMMnhYN5YZUL2VropA-7P1xWk"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.event
async def on_message(message):
    your_desired_channel_id = "596754054710034451"
    if message.author == client.user:
        pass
    elif message.channel != client.get_channel(your_desired_channel_id):
        pass
    else:
        nick = message.author.display_name
        channel = client.get_channel(your_desired_channel_id)
        msg = message.content
        # data = str(nick)+": "+str(msg)
        # s.say(data)
        await client.say(msg)
        # await message.channel.purge(limit=1)
        # await channel.send('```diff\n+ {0}: {1}```'.format(nick, msg))


@client.command()
async def spam(number):
    # await client.say(f"You said {number}")
    await client.say(f"{client.get_all_channels()}, {client.get_all_members()}, {client.get_channel()}, {client.get_message()}")


@client.command()
async def repeat(number):
    # squared_value = int(number) * int(number)
    await client.say(f"You said {number}")


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with my 'vacuum cleaner'"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)