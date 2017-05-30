"""AutomaBot package."""

import sys

from .config import token, bot_command_prefix, bot_description, HOST, PORT, update_channel_id
from .tools import make_embed_message, send_waiting_message
from .web import make_app
from .automaBot import AutomaBot

if sys.version_info < (3, 6):
    raise ImportError("automabot requires Python 3.6+ because f-str/asyncio. "
                      "<3")
