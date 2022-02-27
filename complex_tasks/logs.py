import discord, os
from client import client
from database import Database
from datetime import datetime
from dotenv import load_dotenv
from functions import discord_file

load_dotenv('.env')

def embed_creation(message: discord.Message) -> discord.Embed:

    embed = discord.Embed(colour=message.author.color, timestamp=datetime.utcnow())
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.set_author(name=f"Wiadomosc usunięta")
    embed.add_field(name='Kanał', value=message.channel, inline=False)

    if len(message.content) > 0:
        embed.add_field(name='Treść', value=message.content, inline=False)
    else:
        embed.add_field(name='Treść', value='Brak zawartości', inline=False)

    if len(message.attachments) > 0:
        embed.add_field(name='Ilość załączników:', value=len(message.attachments), inline=False)

    embed.set_footer(text=f'{message.author.name} {message.author.id}', icon_url=message.author.avatar_url)
    return embed

@client.event
async def on_message_delete(message):
    db = Database(os.getenv('DB_NAME'))
    logs_channel = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    logs_channel = client.get_channel(logs_channel[0])

    if any(temp in message.content for temp in ['-hug', '-lick', '-pat', '-boop', '-kiss']) or message.channel == logs_channel or message.author.bot:
        return

    if not message.content.startswith('.') and not message.content.startswith('-'):
        client.snipe = {"author": message.author.name, "content": message.content, "id": message.author.id}

    else:
        return
    
    embed = embed_creation(message)

    await logs_channel.send(embed=embed)

@client.event
async def on_bulk_message_delete(messages):

    db = Database(os.getenv('DB_NAME'))
    logs_channel = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    logs_channel = client.get_channel(logs_channel[0])
    
    for message in messages:    
        if any(temp in message.content for temp in ['-hug', '-lick', '-pat', '-boop', '-kiss']) or message.channel.id == 559910981392793601 or message.author.bot:
            continue

        if message.content.startswith('.') or message.content.startswith('-'):
            continue

        embed = embed_creation(message)

        await logs_channel.send(embed=embed)

@client.event
async def on_message(message):

    await client.process_commands(message)

    if len(message.attachments) > 0 and not message.author.bot:
        for att in message.attachments:
            await att.save(f'graphic_logs/{message.id}_{att.id}_{att.filename}')
        if len(os.listdir('graphic_logs')) > 50:
            for file_name in sorted(os.listdir('graphic_logs'), key=lambda f: os.stat(f'graphic_logs/{f}').st_mtime, reverse=True)[50:]:
                os.remove(f'graphic_logs/{file_name}')

@client.event
async def on_raw_message_delete(payload):

    message_id = payload.message_id
    db = Database(os.getenv('DB_NAME'))
    logs_channel = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    logs_channel = client.get_channel(logs_channel[0])

    for name in os.listdir('graphic_logs'):
        if str(message_id) in name:

            deleted_att = discord_file(f'graphic_logs/{name}', name, False)
            await logs_channel.send('Usunięty plik', file=deleted_att)
            os.remove(f'graphic_logs/{name}')

@client.event
async def on_raw_bulk_message_delete(payload):
    db = Database(os.getenv('DB_NAME'))
    logs_channel = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    logs_channel = client.get_channel(logs_channel[0])

    for message_id in payload.message_ids:

        for name in os.listdir('graphic_logs'):
            if str(message_id) in name:

                deleted_att = discord_file(f'graphic_logs/{name}', name, False)
                await logs_channel.send('Usunięty plik', file=deleted_att)
                os.remove(f'graphic_logs/{name}')

@client.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content:
        return

    await client.process_commands(after)

    embed = discord.Embed(colour=after.author.colour, timestamp=datetime.utcnow())
    embed.set_author(name=f"Wiadomosc edytowana")
    embed.set_thumbnail(url=after.author.avatar_url)
    embed.add_field(name="Kanał:", value=after.channel, inline=False)
    embed.add_field(name='Przed', value=before.content, inline=False)
    embed.add_field(name='Po', value=after.content, inline=False)
    embed.set_footer(text=f'{after.author.name} {after.author.id}', icon_url=after.author.avatar_url)

    db = Database(os.getenv('DB_NAME'))
    logs_channel = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    logs_channel = client.get_channel(logs_channel[0])
    await logs_channel.send(embed=embed)