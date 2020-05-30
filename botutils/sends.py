"""Contains functions to send messages"""

import configparser
import enum
from .helpers import make_ping

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
LOGGING_CHANNEL_ID = Config["user"]["LOGGING_CHANNEL_ID"]
OWNER_ID = Config["user"]["OWNER_ID"]
MAX_MESSAGE_LEN = Config["misc"]["MAX_MESSAGE_LEN"]


class Level(enum.Enum):
    """Level of logging"""
    info = "[INFO]"
    warning = "**[WARNING]**"
    error = "**[ERROR]**"


async def __send_log(client, message):
    """Send a message to the logs"""
    log_channel = client.get_channel(int(LOGGING_CHANNEL_ID))
    await log_channel.send(message)


def __create_python_code_block(client, message):
    """Create a python code block"""
    return f"```python\n{message}```"


async def __send_long_error(client, post, depth=0):
    """Send a message and break it down if it goes over the Discord message limit"""
    max = int(MAX_MESSAGE_LEN) - 50
    if len(post) <= max:
        if depth:
            await __send_log(client, "[CONTINUED] " + "```py\n" + post[:max])
        else:
            await __send_log(client, post)
            return
    else:
        if depth:
            await __send_log(client, "[CONTINUED] " + "```py\n" + post[:max] + "```")
        else:
            await __send_log(client, post[:max] + "```")
        await __send_long_error(client, post[max:], depth + 1)


async def log(client, level, message):
    """Send a message to the logs with a header"""
    if level == Level.error:
        msg = f"{level.value} {make_ping(OWNER_ID)}\n{__create_python_code_block(client, message)}"
        await __send_long_error(client, msg)
    else:
        msg = f"{level.value} {message}"
        await __send_log(client, msg)


async def send_lobby(client, message):
    """Send a message to the lobby"""
    lobby_channel = client.get_channel(int(LOBBY_CHANNEL_ID))
    await lobby_channel.send(message)
