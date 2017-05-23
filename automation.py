from automa_tools import Automa_tools
import discord
import asyncio
import requests
from tools import make_embed_message

class Automation(Automa_tools):
    """
    Class used in AutomaBot to make everything related to automation.
    """
    def __init__(self, example, type, filename, client):
        self.example = example
        self.description = "Enters " + type + " functionalities"
        self.filename = filename
        self.client = client
        self.funcs_desc = {
                    "lightstates" : "Returns lights states",
                    "setlight [light] [state]" : "Sets [light] state to [state]",
                    "get_forecast" : "Returns where to find the code for your nearest city",
                    "get_forecast [location]":"Returns forecasts for current and next 4 days at [location]"}


        self.load_parameter()

    async def lightstates(self, message, tmp):
        """contacts the api to get light status and sends it"""
        r = requests.get(self.parameter_list["url_get"])
        embed = make_embed_message("**Lights states**", message, eval(r.text), self.client)
        await self.client.edit_message(tmp, new_content='Right now : ', embed=embed)


    async def setlight(self, message, tmp, lamp_and_state):
        """set lamp state to the state needed and returns server response
            TODO: improve this function to detect api errors.
        """
        msg_split = lamp_and_state.split(' ')
        if len(msg_split)>1:
            payload= {'lamp': msg_split[0], 'state': msg_split[1]}
            r = requests.post(self.parameter_list["url_post"], data=payload)
            msg = 'Changed {lamp} to {state}'.format(lamp=msg_split[0], state=r.text)
            await self.client.edit_message(tmp, new_content=msg)
        else:
            await self.client.edit_message(tmp, new_content='You forgot parameters...\ndo you ride bikes with no wheels?... use *!automation* for help ')

    async def get_forecast(self, message, tmp, location=""):
        """ Contacts a distant server and gets forecats for the location needed.
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
                await self.client.send_file(message.channel, msg)
            await self.client.edit_message(tmp, new_content="Forecast for "+location+":")
        else:
            msg = 'To see all available cities, check this site : http://www.prevision-meteo.ch/services/json/list-cities'
            await self.client.edit_message(tmp, new_content=msg)
