"""Contains functions to send messages"""

import configparser
import enum

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
LOGGING_CHANNEL_ID = Config["user"]["LOGGING_CHANNEL_ID"]

class Level(enum.Enum):
    """Level of logging"""
    info = "[INFO]"
    warning = "**[WARNING]**"
    error = "**[ERROR]**"

async def __send_log(client, message):
    """Send a message to the logs"""
    log_channel = client.get_channel(int(LOGGING_CHANNEL_ID))
    await log_channel.send(message)

async def log(client, level, message):
    """Send a message to the logs with a header"""
    msg = f"{level.value} {message}"
    await __send_log(client, msg)

async def send_lobby(client, message):
    """Send a message to the lobby"""
    lobby_channel = client.get_channel(int(LOBBY_CHANNEL_ID))
    await lobby_channel.send(message)