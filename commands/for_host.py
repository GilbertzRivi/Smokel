from client import client
from database import Database
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

@client.command()
async def off(ctx):
    if ctx.author != ctx.author.guild.owner:
        return

    await client.close()

@client.command()
async def set_guild(ctx):
    if ctx.author != ctx.author.guild.owner:
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="guild_id"')
    db.insert('config', None, 'guild_id', ctx.guild.id, None)
    result = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(result[0])
    await ctx.send(f'Pomyślnie ustawiono serwer na {guild.name}')