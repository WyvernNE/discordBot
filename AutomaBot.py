import discord
import asyncio
import requests
import datetime
from random import choice
import pickle

client = discord.Client()
botUsername = ""
commands = {}
commands["!light"]="Returns light states"
commands["!setlight \{light\} \{state\}"]="Set \{light\} state to \{state\}"
#jokes = ["Drinking gasoline", "Burning water", "Painting it black", "Caressing a dragon", "Climbing Down", "Eating bees", "Falling up", "Dancing macarena", "cooking some meths","Calling for mr.White"]
sleep = False
jokes = []
authorized_users={'Maël Pedretti#1416' : 0, 'Wyll Vern#4651' :1}

@client.event
async def on_ready():
    global botUsername
    botUsername = client.user.name + "#" + client.user.discriminator
    print('Logged in as')
    print(botUsername)
    print('------')
    #await say_hi_to_everyone()
    load_parameters()

def load_parameters():
    global jokes
    jokes = load_parameter('jokes.txt')
    global authorized_users
    authorized_users = load_parameter('authorized_users.txt')

def load_parameter(filename):
    with open (filename, 'rb') as fp:
        parameter = pickle.load(fp)
    return parameter

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
    if message.content[0] != "!":
        return 0

    #si l'utilisateur n'as pas le droit d'utiliser le bot, tant pis pour lui
    if str(message.author) not in authorized_users:
        msg = 'I am not allowed to talk to you ! :no_mouth:\n Please don\'t contact {0.mention} (server admin) to complain...'.format(list(client.servers)[0].owner)
        await client.send_message(message.channel, msg)
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



    if message.content.startswith('!sleep'):
        sleep=True
        await client.change_presence(status=discord.Status.dnd, afk=False)
        msg = 'Going to sleep. See you :wave:'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!help'):
        tmp = await client.send_message(message.channel, choice(jokes))
        embed = make_embed_message("**Automation commands**", message, commands)
        await client.edit_message(tmp, new_content='Finished : ', embed=embed)

    elif message.content.startswith('!test'):
        msg = 'You shouldn\'t test my patience...'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!light'):
        tmp = await client.send_message(message.channel, choice(jokes))
        r = requests.get('http://localhost:8000/light-natural')
        embed = make_embed_message("**Lights states**", message, eval(r.text))
        await client.edit_message(tmp, new_content='Right now : ', embed=embed)

    elif message.content.startswith('!setlight'):
        tmp = await client.send_message(message.channel, choice(jokes))
        msg_split = message.content.split(' ')
        if len(msg_split)>1:
            payload= {'lamp': msg_split[1], 'state': msg_split[2]}
            r = requests.post("http://localhost:8000/light", data=payload)
            msg = 'Changed {lamp} to {state}'.format(lamp=msg_split[1], state=r.text)
            await client.edit_message(tmp, msg)
        else:
            embed = make_embed_message("**Automation commands**", message, commands)
            await client.edit_message(tmp, new_content='You forgot parameters...\ndo you ride bikes with no wheels?... : ', embed=embed)

    elif message.content.startswith('!weather'):
        await get_forecast(message)

    elif message.content.startswith('!newjoke'):
        filename = 'jokes.txt'
        await update_list(message, jokes, filename)

    elif message.content.startswith('!newuser'):
        filename = 'authorized_users.txt'
        await update_list(message, authorized_users, filename)

    elif message.content.startswith('!removeuser'):
        filename = 'authorized_users.txt'
        await update_list(message, authorized_users, filename, False)

    elif message.content.startswith('!listjokes'):
        await list_from_variable(message, jokes)

    elif message.content.startswith('!listusers'):
        await list_from_variable(message, authorized_users)

    else:
        msg = "Sorry, this command is unknown to me... :japanese_ogre: "
        await client.send_message(message.channel, msg)

async def update_list(message, var, filename, add=True):
    msg_split = message.content.split(' ', 1)
    if len(msg_split)>1:
        if add:
            var.append(msg_split[1])
        else:
            var.remove(msg_split[1])

        with open(filename, 'wb') as fp:
            pickle.dump(var, fp)
        msg = 'Done!'
    else:
        msg = 'You must specify something to change! :rolling_eyes: '

    await client.send_message(message.channel, msg)

async def list_from_variable(message, var):
    if len(var) != 0:
        msg = ""
        for _ in var:
            msg += _ + "\n"
    else:
        msg = "No content for the moment "
    await client.send_message(message.channel, msg)

async def get_forecast(message):
    msg_split = message.content.split(' ', 1)
    if len(msg_split)>1:
        for i in range(5):
            directory = 'pictures/'
            pic_name = '{city}_{day}.png'.format(city = msg_split[1], day=i)
            with open(directory+pic_name, 'wb') as handle:
                response = requests.get('http://www.prevision-meteo.ch/uploads/widget/'+pic_name, stream=True)

                if response.ok:
                    msg = directory+pic_name
                else:
                    msg = response

                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

            await client.send_file(message.channel, msg)
    else:
        msg = 'To see all available cities, check this site : http://www.prevision-meteo.ch/services/json/list-cities'
        await client.send_message(message.channel, msg)


def make_embed_message(title, message, datas):
    #embed properties
    embed_title = title
    embed_colour = discord.Colour(0x26A65B)
    embed_timestamp = datetime.datetime.utcfromtimestamp(1495179665)
    embed = discord.Embed(title=embed_title, colour=embed_colour, timestamp=embed_timestamp)

    #author properties
    author_name = message.author
    author_url = "https://discordapp.com"
    author_icon_url = message.author.avatar_url
    embed.set_author(name=author_name, url=author_url, icon_url=author_icon_url)

    #footer properties
    footer_text = client.user.name
    footer_icon_url = client.user.avatar_url
    embed.set_footer(text=footer_text, icon_url=footer_icon_url)

    inline = False
    for key, value in datas.items():
        embed.add_field(name=key, value=value, inline=inline)

    return embed

client.run('MzE0Nzg1Njg0NzYwMDM1MzI4.C_9OiQ.Jw2oZoxgnZb5ji5q-CnQdW_2UkM')
