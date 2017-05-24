from automa_tools import Automa_tools
import discord
import asyncio
import requests
from tools import make_embed_message, send_waiting_message
from discord.ext import commands

#TODO regarder s'il n'y a pas de fonction pour ajouter des commandes à un cog, sinon +++++essayer bot.add_command()
# de ce fait, il sera possible d'utiliser les décorateurs

class Automation(Automa_tools):


    """
    Class used in AutomaBot to make everything related to automation.
    """
    def __init__(self, example, type, filename, bot):
        self.example = example
        self.description = "Enters " + type + " functionalities"
        self.filename = filename
        self.bot = bot
        self.dir = "config/"

        self.load_parameter()

    @commands.command()
    async def lightstates(self, message, tmp):
        """
        Returns lights status
        Contacts the api to get light status writes it as a list"""
        r = requests.get(self.parameter_list["url_get"])
        embed = make_embed_message("**Lights states**", message, eval(r.text), self.bot)
        await self.bot.edit_message(tmp, new_content='Right now : ', embed=embed)

    @commands.command()
    async def setlight(self, message, tmp, lamp_and_state):
        """ Sets lamp state
            Changes state of lamp to state (both contained in lamp_and_state and sending server response
            TODO: improve this function to detect api errors.
        """
        msg_split = lamp_and_state.split(' ')
        if len(msg_split)>1:
            payload= {'lamp': msg_split[0], 'state': msg_split[1]}
            r = requests.post(self.parameter_list["url_post"], data=payload)
            msg = 'Changed {lamp} to {state}'.format(lamp=msg_split[0], state=r.text)
            await self.bot.edit_message(tmp, new_content=msg)
        else:
            await self.bot.edit_message(tmp, new_content='You forgot parameters...\ndo you ride bikes with no wheels?... use *!automation* for help ')


    @commands.command()
    async def get_forecast(self, message, tmp, location=""):
        """
        Returns forecasts for the specified location.
        If no location is supplied, sends the link where you can find the nearest city
        """
        msg_split = message.content.split(' ', 1)
        if location != "":
            for i in range(5):
                directory = 'pictures/'
                pic_name = '{city}_{day}.png'.format(city = location, day=i)
                with open(directory+pic_name, 'wb') as handle:
                    response = requests.get(self.parameter_list["weather_widget"]+pic_name, stream=True)

                    if response.ok:
                        msg = directory+pic_name
                    else:
                        msg = response

                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                await self.bot.send_file(message.channel, msg)
            await self.bot.edit_message(tmp, new_content="Forecast for "+location+":")
        else:
            msg = 'To see all available cities, check this site : http://www.prevision-meteo.ch/services/json/list-cities'
            await self.bot.edit_message(tmp, new_content=msg)
