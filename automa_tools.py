import json
import discord
import asyncio
import requests
from random import choice
class Automa_tools:
    """
    Class used in AutomaBot to list users who are authorized to use the bot and jokes sent while waiting for embed messages.
    """
    def __init__(self, example, type, filename, client):
        self.example = example
        self.description = "Enters " + type + " functionalities"
        self.filename = filename
        self.client = client
        self.funcs_desc = {
                            "add ["+type+"]" : "Adds ["+type+"] to list",
                            "remove ["+type+"]" : "Removes ["+type+"] from list",
                            "list" : "Lists parameters in the list"}

        self.load_parameter()
        print

    async def add(self, message, tmp, to_add):
        """
        Name : Add
        Example : add [element]
        Description : Adds an element to the list
        """
        msg = self.update_list(to_add, message)
        await self.client.edit_message(tmp, new_content=msg)


    async def remove(self, message,tmp, to_remove):
        """
        Name : Remove
        Example : remove [element]
        Description : Removes an element to the list
        """
        msg = self.update_list(to_remove,message, False)
        await self.client.edit_message(tmp, new_content=msg)

    async def list(self, message, tmp):
        """
        Name : List
        Example : list
        Description : Lists parameters in the list
        """
        if len(self.parameter_list) != 0:
            msg = ""
            for _ in self.parameter_list:
                msg += _ + "\n"
        else:
            msg = "No content for the moment "
        await self.client.edit_message(tmp, new_content=msg)

    def update_list(self, var, message, add=True):
        """
        Updates var from var, and store it in file represented by filename.
        add defines the operation. Add or remove.
        """
        msg_split = message.content.split(' ', 1)
        if len(msg_split)>1:
            if add:
                self.parameter_list.append(var)
            else:
                self.parameter_list.remove(var)

            with open(self.filename, 'w', encoding="utf-8") as fp:
                json.dump(self.parameter_list, fp)
                msg = 'Done!'
        else:
            msg = 'You must specify something to change! :rolling_eyes: '

        return msg

    def load_parameter(self):
        """
        Loads parameters stored in self.filename.
        """
        with open ("config/"+self.filename, 'rb') as fp:
            self.parameter_list = json.load(fp)
