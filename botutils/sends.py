"""Contains functions to send messages"""

import configparser
import enum
import json
import globvars
from .helpers import make_ping

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]
SERVER_ID = int(SERVER_ID)
LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
LOBBY_CHANNEL_ID = int(LOBBY_CHANNEL_ID)
LOGGING_CHANNEL_ID = Config["user"]["LOGGING_CHANNEL_ID"]
LOGGING_CHANNEL_ID = int(LOGGING_CHANNEL_ID)
OWNER_ID = Config["user"]["OWNER_ID"]
OWNER_ID = int(OWNER_ID)
MAX_MESSAGE_LEN = Config["misc"]["MAX_MESSAGE_LEN"]
MAX_MESSAGE_LEN = int(MAX_MESSAGE_LEN)


with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

stats_pregame_header = language["cmd"]["stats_pregame_header"]


class Level(enum.Enum):
    """Level of logging"""
    info = "[INFO]"
    warning = "**[WARNING]**"
    error = "**[ERROR]**"


async def __send_log(message):
    """Send a message to the logs"""
    log_channel = globvars.client.get_channel(int(LOGGING_CHANNEL_ID))
    await log_channel.send(message)


def __create_python_code_block(message):
    """Create a python code block"""
    return f"```python\n{message}```"


def __create_code_block(message):
    """Create a python code block"""
    return f"```\n{message}```"


async def send_pregame_stats(ctx, id_list):
    """Send the pregame stats board"""
    msg = ctx.author.mention + " " + stats_pregame_header.format(len(id_list))
    temp = "\n"
    for userid in id_list:
        member = globvars.client.get_guild(SERVER_ID).get_member(int(userid))
        name = member.display_name
        temp += f"{name} ({userid})\n"
    temp = __create_code_block(temp)
    msg += temp
    await ctx.send(msg)


async def __send_long_error(post, depth=0):
    """Send a message and break it down if it goes over the Discord message limit"""
    max = int(MAX_MESSAGE_LEN) - 50
    if len(post) <= max:
        if depth:
            await __send_log("[CONTINUED] " + "```py\n" + post[:max])
        else:
            await __send_log(post)
            return
    else:
        if depth:
            await __send_log("[CONTINUED] " + "```py\n" + post[:max] + "```")
        else:
            await __send_log(post[:max] + "```")
        await __send_long_error(post[max:], depth + 1)


async def log(level, message):
    """Send a message to the logs with a header"""
    if level == Level.error:
        msg = f"{level.value} {make_ping(OWNER_ID)}\n{__create_python_code_block(message)}"
        await __send_long_error(msg)
    else:
        msg = f"{level.value} {message}"
        await __send_log(msg)


async def send_lobby(message, embed = None, file = None):
    """Send a message to the lobby"""
    lobby_channel = globvars.client.get_channel(int(LOBBY_CHANNEL_ID))
    ret = await lobby_channel.send(message, embed=embed, file = file)
    return ret
