from client import client
from database import Database
from functions import discord_file, user_info
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')

@client.event
async def on_member_join(member):
    
    db = Database(getenv('DB_NAME'))
    result = db.fetch_all('*', 'black_list')
    for row in result:
        if row[1] == member.id:
            await member.ban(reason='Black lista')
            main_channel = db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
            main_channel = client.get_channel(main_channel[0])
            await main_channel.send(f'{member.name} nie dostał się na serwer gdyż był na blackliście')
            db.delete('black_list', f'banned_id={member.id}')
            return
    
    welcoming = f"""
Witamy serdecznie {member.display_name} na serwerze FurHeaven. 
Celem tego miejsca jest zrzeszanie osob interesujacych sie tematyka furry. 
Jest tu sporo osob z ktorymi mozna pogadac na przerozne tematy. Mamy nadzieje, 
ze bedzie Ci tu z nami milo :grin:
Odpowiedz tylko na cztery pytania.

1. Ile masz lat?
2. Czy jestes futrzakiem?
3. Czy przeczytales regulamin i bedziesz go przestrzegac?
4. Skąd masz zaproszenie?

Jeżeli odpowiedziałeś/aś na pytania a nikt z moderacji ani administracji jeszcze Cię nie zweryfikował,
oznacz któregoś z nich, na pewno od razu przeprowadzą weryfikację :3"""
    
    veryfication_channel = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
    veryfication_channel = client.get_channel(veryfication_channel[0])
    main_channel =  db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
    main_channel = client.get_channel(main_channel[0])
    dividing_roles_ids = db.fetch('value', 'config', 'grp="dividing_roles"').fetchall()
    command_channel = db.fetch('value', 'config', 'name="command_channel_id"').fetchone()
    command_channel = client.get_channel(command_channel[0])
    
    image = discord_file('resources/join_veryfication.gif', 'Witamy.gif', False)
    message_with_image = await veryfication_channel.send(content=welcoming, file=image)
    
    message_on_main = await main_channel.send(f"<@{member.id}> wlasnie wbil/a na serwer! Zaraz powinien/na do nas dolaczyc.")
    
    for role_id in dividing_roles_ids:
        await member.add_roles(member.guild.get_role(role_id[0]))
    
    user_info_embed = user_info(author=member, member=member, new=True)
    await command_channel.send(embed=user_info_embed)
    
    message_with_mention = await veryfication_channel.send(f'<@{member.id}>')

    db.insert('veryfication', None, f'{member.id}', f'{message_with_image.id}', member.joined_at.timestamp())
    db.insert('veryfication', None, f'{member.id}', f'{message_with_mention.id}', member.joined_at.timestamp())

@client.event
async def on_member_remove(member):
    
    db = Database(getenv('DB_NAME'))
    veryfication_channel_id = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
    main_channel_id = db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
    veryfication_channel = await client.fetch_channel(veryfication_channel_id[0])
    main_channel = await client.fetch_channel(main_channel_id[0])
    
    result = db.fetch('message_id', 'veryfication', f'person_id={member.id}').fetchall()
    if result is not None:
        for message_id in result:
            message = await veryfication_channel.fetch_message(message_id[0])
            await message.delete()
        
    if client.silent_ban == member.id or client.silent_kick == member.id:
        return
        
    bans = await member.guild.bans()
    if member.id in [ban.user.id for ban in bans]:
        image = discord_file('resources/banned.gif', 'Only gulag for ya~.gif', False)
        await main_channel.send(f'{member.name} dostał bana', file=image)
        return

    member_join_timestamp = db.fetch('join_time', 'veryfication', f'person_id={member.id}').fetchone()
    db.delete('veryfication', f'person_id={member.id}')
    if member_join_timestamp is not None:
        if datetime.now().timestamp() - member_join_timestamp[0] - 3600 < 60:
            async for msg in main_channel.history(limit=100):
                if member.mention in msg.content and msg.author == client.user:
                    await msg.delete()

            await main_channel.send(f'{member.name} niestety nie wytrzymał presji weryfikacji')
    else:
        await main_channel.send(f'{member.name} opuścił serwer')

@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author != client.user:

        db = Database(getenv('DB_NAME'))
        veryfication_channel_id = db.fetch('value', 'config', 'name="veryfication_channel_id"').fetchone()
        veryfication_channel = await client.fetch_channel(veryfication_channel_id[0])

        result = db.fetch('*', 'veryfication', f'person_id="{message.author.id}"').fetchone()
        if message.channel == veryfication_channel and result is not None:
            db.insert('veryfication', None, f'{message.author.id}', f'{message.id}', message.author.joined_at.timestamp())

@client.event
async def on_raw_message_delete(payload):
    db = Database(getenv('DB_NAME'))
    db.delete('veryfication', f'message_id={payload.message_id}')

@client.event
async def on_member_update(before, after):
    db = Database(getenv('DB_NAME'))
    guild = db.fetch('value', 'config', 'name="guild_id"').fetchone()
    veryfied_role = db.fetch('value', 'config', 'name="veryfied_role_id"').fetchone()
    muted_role = db.fetch('value', 'config', 'name="mute_role_id"').fetchone()
    main_channel = db.fetch('value', 'config', 'name="main_channel_id"').fetchone()
    guild = client.get_guild(guild[0])
    veryfied_role = guild.get_role(veryfied_role[0])
    muted_role = guild.get_role(muted_role[0])
    main_channel = client.get_channel(main_channel[0])
    
    if veryfied_role in after.roles and veryfied_role not in before.roles and muted_role not in before.roles and muted_role not in after.roles:
        await main_channel.send(f'Witamy na głównym kanale {after.mention} <:sup:726535134890688533>', file=discord_file('resources/witamy_na_fh.mp4', 'witamy_w_kolonii.mp4', False))
