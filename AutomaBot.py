from discord.ext import commands
import discord
import asyncio
import requests
from random import choice
from automa_tools import User
from automa_tools import Jokes
from automation import Automation
from tools import make_embed_message

description = '''A bot used as front_end for an automation application.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description, self_bot=False)
botUsername = ""

@bot.event
async def on_ready():
    bot.add_cog(Automation("!automation", "automation", "config.json", bot))
    bot.add_cog(Jokes("!jokes", "jokes", "jokes.json", bot))
    bot.add_cog(User("!user", "user", "authorized_users.json", bot))
    global botUsername
    botUsername = bot.user.name + "#" + bot.user.discriminator
    print('Logged in as')
    print(botUsername)
    print('------')
    #await say_hi_to_everyone()

async def say_hi_to_everyone():
    server = list(bot.servers)[0]
    for member in server.members:
        msg = 'Hello {0.mention} I am ready to work\ntype !help if you need help'.format(member)
        await bot.send_message(member, msg)

async def send_error(message):
    msg = "Sorry, this command is unknown to me... :japanese_ogre: Do you need help? If so, just type *!help*"
    await bot.send_message(message.channel, msg)

# BEGIN FUNCTIONS ---------------------------------------------------------------------------------------

@bot.event
async def on_command_error(exception, context):
    if type(exception) is discord.ext.commands.errors.CommandNotFound:
        msg = "This command doesn't exist. Try *!help* to get help. :sunglasses: "
    elif type(exception) is discord.ext.commands.errors.DisabledCommand:
        msg = ":sleeping:"
    elif type(exception) is discord.ext.commands.errors.CommandInvokeError:
        msg=exception.original
    else:
        msg = type(exception)
    await bot.send_message(context.message.channel, msg)

def is_owner(ctx):
    return commands.check(lambda ctx: is_owner_check(ctx.message))

@bot.event
async def on_command_not_found(message):
    bot.say(message)

@bot.command(pass_context=True)
async def hello(ctx):
    """
    Says hello
    """
    msg = f'Hello {ctx.message.author.mention}'
    await bot.say(msg)

@bot.command(pass_context=True, hidden=True)
@commands.check(is_owner)
async def sleep(ctx):
    global awake
    awake = False
    await bot.change_presence(status=discord.Status.dnd, afk=True)
    msg = 'Going to sleep. See you :wave:'
    for comm in bot.commands:
        if comm is not "wakeup":
            bot.commands[comm].enabled=False
    await bot.say(msg)

@bot.command(pass_context=True, hidden=True)
@commands.check(is_owner)
async def wakeup(ctx):
    for comm in bot.commands:
        if comm is not "wakeup":
            bot.commands[comm].enabled=True
    await bot.change_presence(status=discord.Status.online, afk=False)
    msg = 'Goooooooooood morniiing vietnammmmmm :bomb:'
    await bot.say(msg)

async def treat(message):
    """treats message if content matches a known function"""
    global functions
    #if user isn't allowed to use this function, let him know
    if str(message.author) not in functions["!user"].parameter_list:
        msg = 'I am not allowed to let you do this! :no_mouth:\n Please don\'t contact {0.mention} (server admin) to complain...'.format(list(bot.servers)[0].owner)
        await bot.send_message(message.channel, msg)
        return 0

    tmp = await bot.send_message(message.channel, choice(functions["!jokes"].parameter_list))

    msg_split = message.content.split(" ", 1)
    my_commander = functions[msg_split[0]]
    if len(msg_split) == 1:

        embed = make_embed_message("**What do you wand to do? Options are following:**", message, my_commander.funcs_desc, bot)
        await bot.edit_message(tmp, new_content=message.content+ ': ', embed=embed)

        def fct_check(m):
            """checks if function exists in class"""
            invert_op = getattr(my_commander, m.content.split(" ", 1)[0], None)
            if callable(invert_op):
                return True
            return False

        fct = await bot.wait_for_message(timeout=15.0, author=message.author, check=fct_check)
        func_content = fct.content
    else:
        func_split = msg_split[1].split(" ", 1)
        if callable(getattr(my_commander, func_split[0], None)):
            func_content = msg_split[1]
            fct = True
        else:
            await send_error(message)
            return 0

    if fct is None:
        msg = 'Sorry, you took too long. Aborting...'
        await bot.send_message(message.channel, msg)
        return
    else:
        fct_split = func_content.split(" ", 1)
        func = fct_split[0]
        if len(fct_split) > 1:
            param = fct_split[1]
            await getattr(my_commander,func)(message, tmp, param)
        else:
            await getattr(my_commander,func)(message, tmp)

# END FUNCTIONS ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    bot.run('MzE0Nzg1Njg0NzYwMDM1MzI4.C_9OiQ.Jw2oZoxgnZb5ji5q-CnQdW_2UkM')
