from client import client
from database import Database
from dotenv import load_dotenv
from os import getenv
import discord

load_dotenv('.env')

@client.command()
async def set_veryfication_channel(ctx, *, channel: discord.TextChannel):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="veryfication_channel_id"')
    db.insert('config', None, 'veryfication_channel_id', channel.id, None)
    result = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
    channel = client.get_channel(result[0])
    await ctx.send(f'Pomyślnie ustawiono kanał weryfikacyjny na {channel.mention}')

@set_veryfication_channel.error
async def set_veryfication_channel_error(ctx, _):
    await ctx.send('Nie podano kanału')
    
@client.command()
async def set_main_channel(ctx, *, channel: discord.TextChannel):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="main_channel_id"')
    db.insert('config', None, 'main_channel_id', channel.id, None)
    result = db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
    channel = client.get_channel(result[0])
    await ctx.send(f'Pomyślnie ustawiono kanał główny na {channel.mention}')

@set_veryfication_channel.error
async def set_main_channel_error(ctx, _):
    await ctx.send('Nie podano kanału')

@client.command()
async def set_dividing_roles(
    ctx, colores: discord.Role,
    forfun: discord.Role,
    games: discord.Role,
    channels: discord.Role):

    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    name_dict = {
        0: 'dividing_colors',
        1: 'dividing_forfun',
        2: 'dividing_games',
        3: 'dividing_channels'
    }

    db = Database(getenv('DB_NAME'))
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    info_string = ''

    for i, role in enumerate([colores, forfun, games, channels]):
        result = db.fetch('value', 'config', f'name="{name_dict[i]}"').fetchone()
        if result is not None:
            db.delete('config', f'name="{name_dict[i]}"')
        db.insert('config', None, name_dict[i], role.id, 'dividing_roles')
        result = db.fetch('value', 'config', f'name="{name_dict[i]}"').fetchone()
        db_role = guild.get_role(result[0])
        info_string += f'\n{name_dict[i]}: {db_role.name}'
    
    await ctx.send(f'Pomyślnie ustawiono: ```{info_string}```')

@client.command()
async def set_command_channel(ctx, channel: discord.TextChannel):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="command_channel_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="command_channel_id"')
    db.insert('config', None, 'command_channel_id', channel.id, None)
    result = db.fetch('value', 'config', 'name="command_channel_id"').fetchone()
    channel = client.get_channel(result[0])
    await ctx.send(f'Pomyślnie ustawiono kanał komend na {channel.mention}')

@set_veryfication_channel.error
async def set_command_channel_error(ctx, _):
    await ctx.send('Nie podano kanału')

@client.command()
async def set_moderation_role(ctx, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="moderation_role_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="moderation_role_id"')
    db.insert('config', None, 'moderation_role_id', role.id, None)
    result = db.fetch('value', 'config', 'name="moderation_role_id"').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    role = guild.get_role(result[0])
    await ctx.send(f'Pomyślnie ustawiono role moderacyjną na ```{role.name}```')

@set_moderation_role.error
async def set_moderation_role_error(ctx, _):
    await ctx.send('Nie podano roli')

@client.command()
async def set_newbie_role(ctx, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="newbie_role_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="newbie_role_id"')
    db.insert('config', None, 'newbie_role_id', role.id, None)
    result = db.fetch('value', 'config', 'name="newbie_role_id"').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    role = guild.get_role(result[0])
    await ctx.send(f'Pomyślnie ustawiono role newbie na ```{role.name}```')

@set_newbie_role.error
async def set_newbie_role_error(ctx, _):
    await ctx.send('Nie podano roli')

@client.command()
async def set_veryfied_role(ctx, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="veryfied_role_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="veryfied_role_id"')
    db.insert('config', None, 'veryfied_role_id', role.id, None)
    result = db.fetch('value', 'config', 'name="veryfied_role_id"').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    role = guild.get_role(result[0])
    await ctx.send(f'Pomyślnie ustawiono role zweryfikowanego na ```{role.name}```')

@set_veryfied_role.error
async def set_veryfied_role_error(ctx, _):
    await ctx.send('Nie podano roli')

@client.command()
async def set_mute_role(ctx, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="mute_role_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="mute_role_id"')
    db.insert('config', None, 'mute_role_id', role.id, None)
    result = db.fetch('value', 'config', 'name="mute_role_id"').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    role = guild.get_role(result[0])
    await ctx.send(f'Pomyślnie ustawiono role mute\'a na ```{role.name}```')

@set_mute_role.error
async def set_mute_role_error(ctx, _):
    await ctx.send('Nie podano roli')

@client.command()
async def set_logs_channel(ctx, role: discord.TextChannel):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return

    db = Database(getenv('DB_NAME'))
    result = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    if result is not None:
        db.delete('config', 'name="logs_channel_id"')
    db.insert('config', None, 'logs_channel_id', role.id, None)
    result = db.fetch('value', 'config', 'name="logs_channel_id"').fetchone()
    channel = client.get_channel(result[0])
    await ctx.send(f'Pomyślnie ustawiono kanał logów na ```{channel.name}```')

@set_logs_channel.error
async def set_logs_channel_error(ctx, _):
    await ctx.send('Nie podano kanału')

@client.command()
async def exclude(ctx, *, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Nie masz uprawnień')
        return
        
    db = Database(getenv('DB_NAME'))
    result = db.fetch('is_excluded', 'autoroles', f'role_id={role.id}').fetchone()
    if result is not None:
        db.delete('autoroles', f'role_id={role.id}')
    db.insert('autoroles', role.id, None, None, 1)
    result = db.fetch('role_id', 'autoroles', f'role_id={role.id}').fetchone()
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    guild = client.get_guild(guild[0])
    role = guild.get_role(result[0])
    await ctx.send(f'Pomyślnie wyłączono z autoroli rolę ```{role.name}```')

@exclude.error
async def exclude_error(ctx, _):
    await ctx.send('Nie podano roli')

