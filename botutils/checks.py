import configparser
import json

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
OWNER_ID = Config["user"]["OWNER_ID"]
ADMINS_ID = json.loads(Config["user"]["ADMINS_ID"])

def __is_lobby(ctx):
    """Check the channel of the context, return True if it is in a private channel."""
    return ctx.channel.id == int(LOBBY_CHANNEL_ID)

def __is_admin(ctx):
    """Check the author of the context, return True if they have admin perms or higher"""
    return ctx.author.id in ADMINS_ID or ctx.author.id == int(OWNER_ID)

def check_if_lobby_or_dm(ctx):
    """Check the channel of the context, return True if it is sent in either 
    lobby or in a private channel or if the user is an admin
    """
    return ctx.guild is None or __is_lobby(ctx) or __is_admin(ctx)