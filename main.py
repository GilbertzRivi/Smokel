from discord.enums import ActivityType
from client import client
from discord import Activity
from os import getenv
from dotenv import load_dotenv
import commands.administration
import commands.entertainment
import commands.for_host
import commands.informative
import commands.moderation
import commands.rest
import complex_tasks.autoroles
import complex_tasks.veryfication
import complex_tasks.logs
import complex_tasks.mute

load_dotenv('.env')
client.silent_ban = ''
client.silent_kick = ''
client.snipe = {"author": None, "content": None, "id": None}

@client.event
async def on_ready():
    print(f'logged in as {client.user.name}')
    await client.change_presence(activity=Activity(name='.help', type=ActivityType.watching))
    complex_tasks.mute.muted_loop.start()
    
client.run(getenv('TOKEN'))