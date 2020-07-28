"""Contains some tasks/async loops"""

import botutils
import json
import asyncio
import discord
import configparser
from discord.ext import tasks

Config = configparser.ConfigParser()
Config.read("config.INI")

ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
ALIVE_ROLE_ID = int(ALIVE_ROLE_ID)
PREFIX = Config["settings"]["PREFIX"]

Config.read("preferences.INI")

LOBBY_TIMEOUT = Config["duration"]["LOBBY_TIMEOUT"]
LOBBY_TIMEOUT = int(LOBBY_TIMEOUT)
TOKEN_RESET = int(Config["duration"]["TOKEN_RESET"])
STATUS_CYCLE = int(Config["duration"]["STATUS_CYCLE"])
START_CLEAR = int(Config["duration"]["START_CLEAR"])

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

lobby_timeout_str = language["system"]["lobby_timeout"]
not_enough_votes_to_start = language["system"]["not_enough_votes_to_start"]


@tasks.loop(seconds = TOKEN_RESET)
async def rate_limit_commands():
    """Rate limit the frequency of commands"""
    import globvars
    for user in globvars.ratelimit_dict:
        globvars.ratelimit_dict[user] = 0
    globvars.logging.info("Cleared the rate limit dict")


@tasks.loop(seconds = LOBBY_TIMEOUT, count=2)
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


@tasks.loop(count = None)
async def cycling_bot_status():
    """A task to cycle bot status messages"""

    messages = [
        "Blood on the Clocktower",
        "{p}help | {p}join".format(p = PREFIX),
        "v0.3.0-alpha"
    ]

    import globvars

    for message in messages:
        activity = discord.Activity(name = message, type = discord.ActivityType.playing)
        await globvars.client.change_presence(activity=activity)
        await asyncio.sleep(STATUS_CYCLE)


@tasks.loop(count = 1)
async def start_votes_timer():
    """A task to clear start votes periodically."""

    import globvars
    await asyncio.sleep(START_CLEAR)
    globvars.start_votes.clear()
    await botutils.send_lobby(not_enough_votes_to_start)

