import discord
import datetime
from random import choice
def make_embed_message(title, message, datas, client):
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
    author_name = message.author
    author_url = "https://github.com/WyllVern/discordBot"
    author_icon_url = message.author.avatar_url
    embed.set_author(name=author_name, url=author_url, icon_url=author_icon_url)

    #footer properties
    footer_text = client.user.name
    footer_icon_url = client.user.avatar_url
    embed.set_footer(text=footer_text, icon_url=footer_icon_url)

    inline = False
    for key, data in datas.items():
        embed.add_field(name=key, value=data, inline=inline)

    return embed

def send_waiting_message(func):
    async def wrapper(*args, **kwargs):
        the_self = args[0]
        ctx = args[1]
        tmp = await the_self.bot.send_message(ctx.message.channel, choice(the_self.bot.get_cog("Jokes").parameter_list))
        args = (the_self, ctx.message, tmp) + args[2:]
        return await func(*args, **kwargs)
    return wrapper
