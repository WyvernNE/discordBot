import json
import discord
import asyncio
import requests
from random import choice
from discord.ext import commands
from tools import send_waiting_message

class Automa_tools:
    """
    Class used in AutomaBot to list users who are authorized to use the bot and jokes sent while waiting for embed messages.
    """
    def __init__(self, example, type, filename, bot):
        self.example = example
        self.description = "Enters " + type + " functionalities"
        self.dir = "config/"
        self.filename = filename
        self.bot = bot

        self.load_parameter()
        print

    @send_waiting_message
    async def add(self, message, tmp, to_add):
        """
        Name : Add
        Example : add [element]
        Description : Adds an element to the list
        """
        msg = self.update_list(to_add, message)
        await self.bot.edit_message(tmp, new_content=msg)

    @send_waiting_message
    async def remove(self, message,tmp, to_remove):
        """
        Name : Remove
        Example : remove [element]
        Description : Removes an element to the list
        """
        msg = self.update_list(to_remove,message, False)
        await self.bot.edit_message(tmp, new_content=msg)

    @send_waiting_message
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
        await self.bot.edit_message(tmp, new_content=msg)

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

            with open(self.dir+self.filename, 'w', encoding="utf-8") as fp:
                json.dump(self.parameter_list, fp)
                msg = 'Done!'
        else:
            msg = 'You must specify something to change! :rolling_eyes: '

        return msg

    def load_parameter(self):
        """
        Loads parameters stored in self.filename.
        """
        with open(self.dir+self.filename, 'rb') as fp:
            self.parameter_list = json.load(fp)

class User(Automa_tools):
    """
    Class used in AutomaBot to work with users who are authorized to use the bot
    """

    @commands.command(pass_context=True)
    async def adduser(self, ctx, to_add):
        """
        Adds an authorized user to the white list
        """
        await self.add(ctx, to_add)

    @commands.command(pass_context=True)
    async def removeuser(self, ctx, to_remove):
        """
        Removes an authorized user from the white list
        """
        await self.remove(ctx, to_remove)

    @commands.command(pass_context=True)
    async def listusers(self, ctx):
        """
        Lists authorized users in the white list
        """
        await self.list(ctx)

class Jokes(Automa_tools):
    """
    Class used in AutomaBot to work with the jokes sent when waiting for something
    """

    @commands.command(pass_context=True)
    async def addjoke(self, ctx, to_add):
        """
        Adds a joke to the joke list
        """
        await self.add(ctx, to_add)

    @commands.command(pass_context=True)
    async def removejoke(self, ctx, to_remove):
        """
        Removes a joke from the joke list
        """
        await self.remove(ctx, to_remove)

    @commands.command(pass_context=True)
    async def listjokes(self, ctx):
        """
        Lists jokes contained in jokes list
        """
        await self.list(ctx)
