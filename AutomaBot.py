from discord.ext import commands
import discord
import asyncio
import requests
from random import choice
from tools import make_embed_message

startup_extensions = ["automation"]

class AutomaBot(commands.Bot):

    def __init__(self, get, update_channel,**options):
        """Init AutomaBot.
        :param get: The Queue reader side.
        :param update_channel: The notification channel id
        :param **options: Default commands.Bot parameters
        """
        super().__init__(**options)
        self.get = get
        self.update_channel=update_channel

    @asyncio.coroutine
    def start(self, *args, **kwargs):
        """|coro|
        A shorthand coroutine for :meth:`login` + :meth:`connect`.

        OVERRIDE
        --------
        Added an extension loader at startup
        """
        self.load_extensions()
        yield from self.login(*args, **kwargs)
        yield from self.connect()

    @asyncio.coroutine
    def run(self, *args, **kwargs):
        """A blocking call that abstracts away the `event loop`_
        initialisation from you.
        If you want more control over the event loop then this
        function should not be used. Use :meth:`start` coroutine
        or :meth:`connect` + :meth:`login`.
        Roughly Equivalent to: ::
            try:
                loop.run_until_complete(start(*args, **kwargs))
            except KeyboardInterrupt:
                loop.run_until_complete(logout())
                # cancel all tasks lingering
            finally:
                loop.close()
        Warning
        --------
        This function must be the last function to call due to the fact that it
        is blocking. That means that registration of events or anything being
        called after this function call will not execute until it returns.

        OVERRIDE
        --------
        Function doesn't run asyncio loop if it is already running.
        """

        try:
            fct = self.start(*args, **kwargs)
            if self.loop.is_running():
                return fct
            else:
                return self.loop.run_until_complete(fct)
        except KeyboardInterrupt:
            self.logout()
            pending = asyncio.Task.all_tasks(loop=self.loop)
            gathered = asyncio.gather(*pending, loop=self.loop)
            try:
                gathered.cancel()
                if self.loop.is_running():
                    gathered
                else:
                    self.loop.run_until_complete(gathered)

                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except:
                pass

    @asyncio.coroutine
    async def on_ready(self):
        """
        When AutomaBot is ready, print its username in console and start notification process
        """
        selfUsername = self.user.name + "#" + self.user.discriminator
        print('Logged in as')
        print(selfUsername)
        print('------')
        await self.notification_handler()

    @asyncio.coroutine
    async def on_command_error(self, exception, context):
        """
        Error handling function.
        """
        if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
            msg = "Sorry, this command is unknown to me... :japanese_ogre: Do you need help? If so, just type *!help* :sunglasses:"
        elif isinstance(exception, discord.ext.commands.errors.DisabledCommand):
            msg = ":sleeping:"
        elif isinstance(exception, discord.ext.commands.errors.CommandInvokeError):
            msg=exception.original
        else:
            msg = type(exception)
        await self.send_message(context.message.channel, msg)

    def load_extensions(self):
        """
        Function used to load extensions at startup.
        Credits go to @leovoel (https://github.com/leovoel). You can find this code here : https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
        """
        for extension in startup_extensions:
            try:
                self.load_extension(extension)
                print(f"loaded extension {extension}")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

    async def notification_handler(self):
        """
        Send a message to the channel specified in config file when datas are available.
        Datas are sent by the api when a light state changes
        """
        while not self.is_closed:
            data = await self.get()
            data["author"]="AutomaBot"
            msg = make_embed_message(title="Update!", datas=data, bot=self)
            channel = self.get_channel(self.update_channel)
            await self.send_message(channel, embed=msg)
