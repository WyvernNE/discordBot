import discord
import asyncio
import requests
from random import choice
from automa_tools import Automa_tools
from automation import Automation
from tools import make_embed_message

client = discord.Client()
botUsername = ""
sleep = False
functions = {
            "!user" : Automa_tools("!user", "user", "authorized_users.json", client),
            "!jokes" : Automa_tools("!jokes", "jokes", "jokes.json", client),
            "!automation" : Automation("!automation", "automation", "config.json", client)
            }

@client.event
async def on_ready():
    global botUsername
    botUsername = client.user.name + "#" + client.user.discriminator
    print('Logged in as')
    print(botUsername)
    print('------')
    #await say_hi_to_everyone()

async def say_hi_to_everyone():
    server = list(client.servers)[0]
    for member in server.members:
        msg = 'Hello {0.mention} I am ready to work\ntype !help if you need help'.format(member)
        await client.send_message(member, msg)

@client.event
async def on_message(message):
    global botUsername
    global commands
    global sleep
    global jokes
    global authorized_users

    #if message doesn't start with an exclamation mark, it isn't destinated to the bot. So do nothing
    if len(message.content) > 0 and message.content[0] != "!":
        return 0

    #if the bot is asleep, the only thing he can do is waking up
    if sleep == True:
        if message.content.startswith('!wakeUp'):
            sleep = False
            msg = 'Goooooooooood morniiing vietnammmmmm :bomb:'

            await client.change_presence(status=None, afk=False)
            await client.send_message(message.channel, msg)
        else:
            return 0

    if message.content.split(" ", 1)[0] in functions:
        await treat(message)

    elif message.content.startswith('!sleep'):
        sleep=True
        await client.change_presence(status=discord.Status.dnd, afk=False)
        msg = 'Going to sleep. See you :wave:'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!help'):
        await get_help(message)

    elif message.content.startswith('!test'):
        msg = 'You shouldn\'t test my patience...'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    else:
        await send_error(message)

async def send_error(message):
    msg = "Sorry, this command is unknown to me... :japanese_ogre: Do you need help? If so, just type *!help*"
    await client.send_message(message.channel, msg)

async def get_help(message):
    jokes = functions["!jokes"].parameter_list
    tmp = await client.send_message(message.channel, choice(jokes))
    desc = {}
    for func in functions:
        desc.update({functions[func].example:functions[func].description})
    embed = make_embed_message("**Commands**", message, desc, client)
    await client.edit_message(tmp, new_content='Finished : ', embed=embed)

# BEGIN FUNCTIONS ---------------------------------------------------------------------------------------


async def treat(message):
    """treats message if content matches a known function"""
    global functions
    #if user isn't allowed to use this function, let him know
    if str(message.author) not in functions["!user"].parameter_list:
        msg = 'I am not allowed to let you do this! :no_mouth:\n Please don\'t contact {0.mention} (server admin) to complain...'.format(list(client.servers)[0].owner)
        await client.send_message(message.channel, msg)
        return 0

    tmp = await client.send_message(message.channel, choice(functions["!jokes"].parameter_list))

    msg_split = message.content.split(" ", 1)
    my_commander = functions[msg_split[0]]
    if len(msg_split) == 1:

        embed = make_embed_message("**What do you wand to do? Options are following:**", message, my_commander.funcs_desc, client)
        await client.edit_message(tmp, new_content=message.content+ ': ', embed=embed)

        def fct_check(m):
            """checks if function exists in class"""
            invert_op = getattr(my_commander, m.content.split(" ", 1)[0], None)
            if callable(invert_op):
                return True
            return False

        fct = await client.wait_for_message(timeout=15.0, author=message.author, check=fct_check)
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
        await client.send_message(message.channel, msg)
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
    client.run('MzE0Nzg1Njg0NzYwMDM1MzI4.C_9OiQ.Jw2oZoxgnZb5ji5q-CnQdW_2UkM')
