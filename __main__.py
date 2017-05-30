"""Main program.

This file is based on @Greut (https://github.com/greut) 's main file in his TravisBot project (https://github.com/greut/travisbot)
"""

import asyncio
import logging
import sys
from automaBot import AutomaBot
from config import token, HOST, PORT, update_channel_id, bot_command_prefix, bot_description
from web import make_app


async def main(token, queue):
    """Run main program."""
    bot = AutomaBot(get=queue, update_channel=update_channel_id, command_prefix=bot_command_prefix, description=bot_description, self_bot=False)
    await bot.run(token)


if __name__ == "__main__":

    if not token or not HOST or not PORT or not update_channel_id or not bot_command_prefix or not bot_description:
        print("Please check your config file. One or more parameter is missing", file=sys.stderr)
        sys.exit(1)

    debug = False

    queue = asyncio.Queue()

    app = make_app(queue.put)

    loop = asyncio.get_event_loop()

    if debug:
        loop.set_debug(True)
        logging.getLogger('asyncio').setLevel(logging.DEBUG)

    handler = app.make_handler(loop=loop)
    loop.run_until_complete(app.startup())

    server = loop.create_server(handler, host=HOST, port=PORT)
    try:
        srv = loop.run_until_complete(server)
        print(f"Listening on {HOST}:{PORT}...\nType Ctrl-C to close.")
        loop.run_until_complete(main(token, queue.get))
    except KeyboardInterrupt:
        pass

    srv.close()
    loop.close()
