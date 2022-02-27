import discord
from database import Database
from client import client
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from asyncio import TimeoutError

load_dotenv('.env')

async def channel_and_message_check(payload):
    channel_id = payload.channel_id
    message_id = payload.message_id

    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    if not message.author.bot:
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('role_id', 'autoroles', f'message_id="{message_id}" and channel_id="{channel_id}"').fetchone()
    if result is None:
        return
    
    role = message.guild.get_role(result[0])
    member = message.guild.get_member(payload.user_id)
    return role, member

@client.command()
async def autoroles(ctx, arg: str):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    await ctx.delete()
    
    db = Database(getenv('DB_NAME'))

    if arg == 'colors':
        await ctx.send('``================``\n  **Role od kolorów**\n``================``')
        first = db.fetch('value', 'config', 'name="dividing_colors"').fetchone()
        last = db.fetch('value', 'config', 'name="dividing_forfun"').fetchone()
    elif arg == 'forfun':
        await ctx.send('``============``\n  **Role for fun**\n``============``')
        first = db.fetch('value', 'config', 'name="dividing_forfun"').fetchone()
        last = db.fetch('value', 'config', 'name="dividing_games"').fetchone()
    elif arg == 'games':
        await ctx.send('``==================``\n   **Pokaż w co grasz**\n``==================``')
        first = db.fetch('value', 'config', 'name="dividing_games"').fetchone()
        last = db.fetch('value', 'config', 'name="dividing_channels"').fetchone()
    elif arg == 'channels':
        await ctx.send('``========================================``\n   **Role funkcyjne, dające dostęp do kanałów\n                   lub pozwalające na ich oznaczenie**\n``========================================``')
        first = db.fetch('value', 'config', 'name="dividing_channels"').fetchone()

    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    first = guild.get_role(first[0])

    if arg == 'channels':
        last = guild.default_role
    else:
        last = guild.get_role(last[0])

    roles = guild.roles[::-1]
    roles = roles[(roles.index(first)+1):(roles.index(last))]
    for role in roles:
        
        result = db.fetch('is_excluded', 'autoroles', f'role_id={role.id}').fetchone()
        if result is not None:
            if result[0] == 1:
                continue

        if arg == 'colors':
            embed = discord.Embed(color=role.color, name=role.name, timestamp=datetime.utcnow())
            embed.add_field(name=role.name, value=f'*hex* - ``{str(role.color).upper()}``')
            embed.set_footer(text=f'-={role.name}=-', icon_url=ctx.guild.icon_url)
            message = await ctx.send(embed=embed)
        else:
            text = f'**{role.name}** - *{role.color}*'
            message = await ctx.send(text)
        
        db.delete('autoroles', f'role_id={role.id}')
        db.insert('autoroles', role.id, message.id, message.channel.id, 0)

        await message.add_reaction('☑')
        try:
            await client.wait_for('reaction_add', timeout=5.0)
        except TimeoutError:
            await message.add_reaction('☑')

@client.event
async def on_raw_reaction_add(payload):
    
    role, member = await channel_and_message_check(payload)
    await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

    role, member = await channel_and_message_check(payload)
    await member.remove_roles(role)
