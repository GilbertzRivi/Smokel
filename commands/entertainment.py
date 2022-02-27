import discord
from client import client
from random import randint
from discord import utils

@client.command()
async def snipe(ctx):
    if client.snipe['content'] == None:
        await ctx.send('Nic do trafienia')
        return

    if randint(1, 2) == 1:
        await ctx.send('Chyba musisz wyregulować przyrządy celownicze, bo to nie było nawet blisko <:kitus:531348685766787077>')
    else:
        
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name='Sniped!')
        embed.add_field(name=client.snipe['author'], value=client.snipe['content'])
        embed.set_footer(text=f'Na prośbę {ctx.author.name}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=utils.get(ctx.guild.members, id=client.snipe['id']).avatar_url)

        await ctx.send(embed=embed)
        
    client.snipe = {"author": None, "content": None, "id": None}