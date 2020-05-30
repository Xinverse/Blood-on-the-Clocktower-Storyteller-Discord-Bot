"""Contains functions to send messages"""

import configparser

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
LOGGING_CHANNEL_ID = Config["user"]["LOGGING_CHANNEL_ID"]

async def send_log(client, message):
    """Send a message to the logs"""
    log_channel = client.get_channel(int(LOGGING_CHANNEL_ID))
    log_channel.send(message)

async def send_lobby(client, message):
    """Send a message to the lobby"""
    lobby_channel = client.get_channel(int(LOBBY_CHANNEL_ID))
    lobby_channel.send(message)