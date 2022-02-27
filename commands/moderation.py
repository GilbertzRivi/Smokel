import discord
from client import client 
from discord.ext import commands
from database import Database
from functions import check_moderator_permissions
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

@client.command()
async def bliad(ctx, id, *, description = 'description not provided'):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return
    
    try: id = int(id)
    except ValueError:
        await ctx.send('błędne id')
        return
    
    db = Database(getenv('DB_NAME'))
    result = db.fetch('*', 'black_list', f'banned_id={id}').fetchone()
    if result is not None:
        db.delete('black_list', f'banned_id={id}')
    db.insert('black_list', None, id, description)

    await ctx.send(f'Pomyślnie dodałem {id} do black listy')

@bliad.error
async def bliad_error(ctx, _):
    await ctx.send('Podano błędny argument')

@client.command()
async def blire(ctx, id):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return
    
    try: id = int(id)
    except ValueError:
        await ctx.send('błędne id')
        return
    
    db = Database(getenv('DB_NAME'))
    
    db.delete('black_list', f'banned_id={id}')
    await ctx.send('Done')
        
@blire.error
async def blire_error(ctx, _):
    await ctx.send('Podano błędny argument')

@client.command()
async def blicheck(ctx):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return
    
    db = Database(getenv('DB_NAME'))
    result = db.fetch_all('*', 'black_list')

    if len([i for i in result]) == 0:
        await ctx.send('Brak wpisów na black liście')
        return
        
    result = db.fetch_all('*', 'black_list')
    
    ids = []
    for row in result:
        ids.append(f"{row[1]} - {row[2]}")
    
    chunked_list = [ids[i:i + 20] for i in range(0, len(ids), 20)]
    
    for i, chunk in enumerate(chunked_list):
        black_list_embed = discord.Embed(color=ctx.author.color, timestamp=datetime.utcnow(), title="Obecny stan blacklisty")
        black_list_embed.add_field(name=i+1, value='\n'.join(chunk), inline=False)
        black_list_embed.set_footer(icon_url=ctx.author.avatar_url, text='Obecny stan black listy')
        await ctx.send(embed=black_list_embed)

@client.command()
async def ban(ctx, member: discord.Member, *, reason = 'Reason not provided'):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    reason = f'{ctx.author.name}: {reason}'
    await member.ban(reason=reason)
    await ctx.send(f'Pomyślnie zbanowałem {member.name}')

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'counters', f'name="{ctx.author.id}_bans"').fetchone()
    if result is None:
        db.insert('counters', f"{ctx.author.id}_bans", 1)
    else:
        db.update('counters', f'value = {result[0] + 1}', f'name="{ctx.author.id}_bans"')

@client.command()
async def sban(ctx, member: discord.Member, *, reason = 'Reason not provided'):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    client.silent_ban = member.id
    reason = f'{ctx.author.name}: {reason}'
    await member.ban(reason=reason)
    await ctx.send(f'Pomyślnie zbanowałem {member.name}')

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'counters', f'name="{ctx.author.id}_bans"').fetchone()
    if result is None:
        db.insert('counters', f"{ctx.author.id}_bans", 1)
    else:
        db.update('counters', f'value = {result[0] + 1}', f'name="{ctx.author.id}_bans"')

@client.command()
async def kick(ctx, member: discord.Member, *, reason = 'Reason not provided'):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    reason = f'{ctx.author.name}: {reason}'
    await member.kick(reason=reason)
    await ctx.send(f'Pomyślnie wyrzuciłem {member.name}')

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'counters', f'name="{ctx.author.id}_kicks"').fetchone()
    if result is None:
        db.insert('counters', f"{ctx.author.id}_kicks", 1)
    else:
        db.update('counters', f'value = {result[0] + 1}', f'name="{ctx.author.id}_kicks"')

@client.command()
async def skick(ctx, member: discord.Member, *, reason = 'Reason not provided'):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    client.silent_kick = member.id
    reason = f'{ctx.author.name}: {reason}'
    await member.kick(reason=reason)
    await ctx.send(f'Pomyślnie wyrzuciłem {member.name}')
    
    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'counters', f'name="{ctx.author.id}_kicks"').fetchone()
    if result is None:
        db.insert('counters', f"{ctx.author.id}_kicks", 1)
    else:
        db.update('counters', f'value = {result[0] + 1}', f'name="{ctx.author.id}_kicks"')

@client.command()
async def accept(ctx, *, member: discord.Member):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return
	
    db = Database(getenv('DB_NAME'))

    await ctx.message.delete()
    
    newbie_role = db.fetch('value', 'config', 'name="newbie_role_id"').fetchone()
    veryfied_role = db.fetch('value', 'config', 'name="veryfied_role_id"').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    newbie_role = guild.get_role(newbie_role[0])
    veryfied_role = guild.get_role(veryfied_role[0])
    await member.add_roles(*(newbie_role, veryfied_role)) 
    
    veryfication_channel_id = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
    veryfication_channel = await client.fetch_channel(veryfication_channel_id[0])
    
    result = db.fetch('message_id', 'veryfication', f'person_id={member.id}').fetchall()
    if result is not None:
        for message_id in result:
            message = await veryfication_channel.fetch_message(message_id[0])
            await message.delete()
        
    db.delete('veryfication', f'person_id={member.id}')

@client.command()
async def purge(ctx, amount):
    try:
        amount = int(amount) + 1
    except ValueError:
        await ctx.channel.send("Twój argument jest inwalidą")
        return

    if ctx.channel.permissions_for(ctx.author).manage_messages:
        await ctx.channel.purge(limit=amount)