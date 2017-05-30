import discord
import datetime
from random import choice

states = {True:'On',False:'Off'}

def make_embed_message(title, datas, bot, message=None):
    """
    Returns a embed message for discord.
    Datas must be a simple dict
    """
    #embed properties
    embed_title = title
    embed_colour = discord.Colour(0x26A65B)
    embed_timestamp = datetime.datetime.utcfromtimestamp(1495179665)
    embed = discord.Embed(title=embed_title, colour=embed_colour, timestamp=embed_timestamp)

    #author properties
    if message is not None:
        author = message.author
        url = message.author.avatar_url
    else:
        author = datas.pop("author")
        url = bot.user.avatar_url

    author_name = author
    author_icon_url = url
    embed.set_author(name=author_name, icon_url=author_icon_url)

    #footer properties
    footer_text = bot.user.name
    footer_icon_url = bot.user.avatar_url
    embed.set_footer(text=footer_text, icon_url=footer_icon_url)

    inline = False
    for key, data in datas.items():
        if data in states:
            data=states[data]
        embed.add_field(name=key.title(), value=data, inline=inline)

    return embed
