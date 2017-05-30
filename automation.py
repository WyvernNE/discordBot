from automaTools import AutomaTools
import discord
import asyncio
import requests
from tools import make_embed_message
from discord.ext import commands
import json

class Automation:
    """
    Class used in AutomaBot to make everything related to automation.
    """
    def __init__(self, filename, bot):
        """Init Automation class.
        :param filename: file containing automation config.
        :param bot: instance of class AutomaBot.
        :attr dir: directory containing config file.
        """
        self.filename = filename
        self.bot = bot
        self.dir = "automation_ressources/"

        self.load_parameter()

    def load_parameter(self):
        """
        Loads parameters stored in self.filename.
        """
        with open(self.dir+self.filename, 'rb') as fp:
            self.parameter_list = json.load(fp)

    @commands.group(pass_context=True)
    async def light(self, ctx):
        """
        Everything that is light related
        """
        return

    @light.command(name='get', pass_context=True)
    async def get(self, ctx):
        """
        Returns lights status
        Contacts the api to get light status and writes it as a list
        """
        tmp = await self.bot.send_message(ctx.message.channel, "Requesting")
        r = requests.get(self.parameter_list["url_get"])
        embed = make_embed_message("**Lights states**", json.loads(r.text), self.bot, ctx.message)
        await self.bot.edit_message(tmp, new_content='Right now : ', embed=embed)

    @light.command(name='set', pass_context=True)
    async def set(self, ctx, lamp, state):
        """
        Sets lamp state
        Changes state of lamp to state (both contained in lamp_and_state and sending server response
        TODO: improve this function to detect api errors.
        TODO: improve this function to send async http requests
        """
        tmp = await self.bot.send_message(ctx.message.channel, "Requesting")
        if lamp is not None and state is not None:
            payload= {'lamp': lamp, 'state': state, 'user_agent': 'AutomaBot'}
            r = requests.post(self.parameter_list["url_post"], data=payload)
            response = json.loads(r.text)
            embed = make_embed_message("*Result!*", response, self.bot, ctx.message)
            await self.bot.edit_message(tmp, new_content='Right now : ', embed=embed)
        else:
            await self.bot.edit_message(tmp, 'You forgot parameters...\ndo you ride bikes with no wheels?... use *!help light* for help ')

def setup(bot):
    """
    Setup cog when using extension autoloader
    """
    bot.add_cog(Automation("config.json", bot))
