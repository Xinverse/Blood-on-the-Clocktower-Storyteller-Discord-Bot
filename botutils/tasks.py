"""Contains some tasks/async loops"""

import configparser
from discord.ext import tasks

Config = configparser.ConfigParser()
Config.read("preferences.INI")

TOKEN_RESET = int(Config["duration"]["TOKEN_RESET"])


@tasks.loop(seconds = TOKEN_RESET)
async def rate_limit_commands():
    """Rate limit the frequency of commands"""
    import globvars
    for user in globvars.ratelimit_dict:
        globvars.ratelimit_dict[user] = 0
    globvars.logging.info("Cleared the rate limit dict")
