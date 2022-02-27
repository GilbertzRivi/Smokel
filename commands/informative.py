import discord
from client import client 
from discord.ext import commands
from database import Database
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

@client.command()
async def check_stats(ctx):
    db = Database(getenv('DB_NAME'))
    kicks = db.fetch('value', 'counters', f'name="{ctx.author.id}_kicks"').fetchone()
    bans = db.fetch('value', 'counters', f'name="{ctx.author.id}_bans"').fetchone()
    result = 'Jeszcze nikogo nie zbanowałeś ani nie wyrzuciłeś z serwera'
    if kicks is not None:
        result += f'wykopałeś: {kicks[0]} osób.\n'
    if bans is not None:
        result += f'zbanowałeś: {bans[0]} osób.'

    if result != 'Jeszcze nikogo nie zbanowałeś ani nie wyrzuciłeś z serwera':
        await ctx.send(result)