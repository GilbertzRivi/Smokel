from discord import client, Intents
from discord.ext import commands

intents = Intents.all()

client = commands.Bot(command_prefix='.', fetch_offline_members=True, intents=intents)
#client.remove_command('help')