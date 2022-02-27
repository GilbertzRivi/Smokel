from client import client
from database import Database
import discord
from discord.ext import tasks
from functions import check_moderator_permissions
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')

@client.command()
async def mute(ctx, muted: discord.Member, *, mute_time):
    if not check_moderator_permissions(ctx.author.roles) and not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    if check_moderator_permissions(muted.roles) or muted.guild_permissions.administrator:
        await ctx.send("Nie mogę zmutować nikogo z zarządu")
        return

    mute_time_timestamp = datetime.now().timestamp()
    for chunk in mute_time.split(' '):
        if 'd' in chunk:
            mute_time_timestamp += int(chunk.strip('d')) * 60*60*24
        elif 'h' in chunk:
            mute_time_timestamp += int(chunk.strip('h')) * 60*60
        elif 'm' in chunk:
            mute_time_timestamp += int(chunk.strip('m')) * 60

    mute_time_from_timestamp = datetime.fromtimestamp(mute_time_timestamp).strftime('%d.%m.%Y, %H:%M')
    await ctx.send(f'Napisz "tak" aby potwierdzić nadanie izolatki {muted.name} do {mute_time_from_timestamp}')

    def check(message):
        return message.content.lower() == 'tak' and message.author == ctx.author and message.channel == ctx.channel
    
    try:
        await client.wait_for('message', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.channel.send('Czas minął')
        return

    db = Database(getenv('DB_NAME'))
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    current_timestamp = datetime.now().timestamp()

    for role in muted.roles[1:]:
        await muted.remove_roles(role, reason='Izolatka')
        db.insert('mutes', None, muted.id, role.id, current_timestamp)

    mute_role = db.fetch('value', 'config', 'name="mute_role_id"').fetchone()
    mute_role = guild.get_role(mute_role[0])

    await muted.add_roles(mute_role, reason='Izolatka')
    await muted.send(f'Zostałeś wyciszony na {guild.name} do {mute_time_from_timestamp}')
    await ctx.channel.send('Wyciszyłem użytkownika')

@tasks.loop(minutes=1)
async def muted_loop():

    current_timestamp = datetime.now().timestamp()
    db = Database(getenv('DB_NAME'))
    mutes = db.fetch_all('*', 'mutes').fetchall()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])

    unmuted = []
    for row in mutes:
        if row[3] < current_timestamp:
            member = guild.get_member(row[1])
            role = guild.get_role(row[2])
            await member.add_roles(role, reason='Koniec izolatki')  
            db.delete('mutes', f'id={row[0]}')  
            unmuted.append(row[1])

    mute_role = db.fetch('value', 'config', 'name="mute_role_id"').fetchone()
    mute_role = guild.get_role(mute_role[0])
    unmuted = list(set(unmuted))
    for member_id in unmuted:
        member = guild.get_member(member_id)
        await member.remove_roles(mute_role)

@muted_loop.error
async def muted_loop_error(_):
    muted_loop.restart()