from client import client
from database import Database
from os import getenv 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')

@client.command()
async def inv(ctx):
    await ctx.message.delete()
    
    db = Database(getenv('DB_NAME'))
    result = db.fetch('timestamp', 'invites', f'user_id={ctx.author.id}').fetchone()
    
    if result is not None:
        if datetime.now().timestamp() - result[0] < 24*60*60:
            await ctx.send('Możesz uzyskać jedno zaproszenie na 24 godziny, jeżeli potrzebujesz następnego poproś o nie kogoś z zarządu')
            return
    
    invite = await ctx.channel.create_invite(max_age=1800, max_uses=1)
    await ctx.author.send(f'Oto zaproszenie dla ciebie {invite.url}\nWażne 30 minut, jedno użycie')
    db.delete('invites', f'user_id={ctx.author.id}')
    db.insert('invites', ctx.author.id, datetime.now().timestamp())
    tech_channel = db.fetch('value', 'config', 'name="tech_channel_id"').fetchone()
    tech_channel = client.get_channel(tech_channel[0]) 
    await tech_channel.send(f'Wysłałem zaproszenie do {ctx.author.name} aka {ctx.author.display_name}')
