"""Contains some tasks/async loops"""

import botutils
import json
import configparser
from discord.ext import tasks

Config = configparser.ConfigParser()
Config.read("preferences.INI")

TOKEN_RESET = int(Config["duration"]["TOKEN_RESET"])

Config.read("config.INI")
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
ALIVE_ROLE_ID = int(ALIVE_ROLE_ID)

Config.read("preferences.INI")
LOBBY_TIMEOUT = Config["duration"]["LOBBY_TIMEOUT"]
LOBBY_TIMEOUT = int(LOBBY_TIMEOUT)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

lobby_timeout_str = language["system"]["lobby_timeout"]


@tasks.loop(seconds = TOKEN_RESET)
async def rate_limit_commands():
    """Rate limit the frequency of commands"""
    import globvars
    for user in globvars.ratelimit_dict:
        globvars.ratelimit_dict[user] = 0
    globvars.logging.info("Cleared the rate limit dict")


@tasks.loop(seconds=LOBBY_TIMEOUT, count=2)
async def lobby_timeout():
    """Lobby timeout loop"""
    pass


@lobby_timeout.after_loop
async def after_lobby_timeout():
    """After lobby timeout"""
    import globvars
    # Only send the lobby timeout message if someone is still in the game
    if not lobby_timeout.is_being_cancelled():
        await botutils.send_lobby(lobby_timeout_str.format(botutils.make_role_ping(ALIVE_ROLE_ID)))
    # Remove the alive role from everyone
    await botutils.remove_all_alive_roles_pregame()
    # Clear the master pregame state
    globvars.master_state.pregame.clear()
    botutils.update_state_machine()

