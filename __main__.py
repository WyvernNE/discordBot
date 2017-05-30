"""Main program.

This file is based on @Greut (https://github.com/greut) 's main file
in his TravisBot project (https://github.com/greut/travisbot)
"""

import asyncio
import json
import logging
import os.path
import sys

from bot import AutomaBot
from tools import load_params
from web import make_app

config_fname = "./config.json"
default_config_fname = "./default_config.json"


async def main(token, queue, channel, prefix, desc):
    """Run main program."""
    bot = AutomaBot(get=queue, update_channel=channel,
                    command_prefix=prefix,
                    description=desc, self_bot=False)
    await bot.run(token)


def my_setup():
    """Set up bot parameters."""
    new_params = {}
    params = load_params(default_config_fname)

    print("""You will now have to set parameters used by the bot.
          Default values are printed between brackets.
          Leave blank if you want to use default value""")

    for param in params:
        new_params[param] = ""
        if not params[param]['value']:
            input_msg = f"{params[param]['def']} : "
        else:
            input_msg = f"{params[param]['def']} [{params[param]['value']}] : "
        while not new_params[param]:
            input_var = input(input_msg)
            if not input_var:
                new_params[param] = params[param]['value']
            else:
                new_params[param] = input_var

    with open(config_fname, 'w', encoding='utf-8') as fp:
        json.dump(new_params, fp)
    sys.exit(1)


if __name__ == "__main__":
    """Catch main function."""

    if not os.path.isfile(config_fname):
        my_setup()

    params = load_params(config_fname)

    HOST = params['HOST']
    PORT = params['PORT']
    token = params['token']
    channel = params['update_channel_id']
    prefix = params['bot_command_prefix']
    desc = params['bot_description']

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
        loop.run_until_complete(main(token, queue.get, channel, prefix, desc))
    except KeyboardInterrupt:
        pass

    srv.close()
    loop.close()
