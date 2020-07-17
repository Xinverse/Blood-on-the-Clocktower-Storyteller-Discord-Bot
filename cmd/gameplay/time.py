"""Contains the time command cog"""

import configparser
import json
import botutils
import traceback
from datetime import datetime, timezone
from discord.ext import commands
from ._gameplay import Gameplay
from botutils import lobby_timeout

Config = configparser.ConfigParser()

Config.read("preferences.INI")
LOBBY_TIMEOUT = Config["duration"]["LOBBY_TIMEOUT"]
LOBBY_TIMEOUT = int(LOBBY_TIMEOUT)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]
lobby_timeout_str = language["system"]["lobby_timeout"]
time_pregame = language["cmd"]["time_pregame"]


class Time(Gameplay, name = language["system"]["gameplay_cog"]):
    """Time command cog"""

    @commands.command(
        pass_context = True, 
        name = "time", 
        aliases = ["t"],
        brief = language["doc"]["time"]["brief"],
        help = language["doc"]["time"]["help"],
        description = language["doc"]["time"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    @commands.check(botutils.check_if_not_in_empty)
    async def time(self, ctx):
        """Time command"""

        import globvars

        # If we are in pregame:
        if globvars.master_state.session == botutils.BotState.pregame:
            now = datetime.now(timezone.utc)
            finish = lobby_timeout.next_iteration
            time_left = finish - now
            time_left = time_left.total_seconds()
            time_left = round(time_left)
            msg = time_pregame.format(botutils.make_time_string(time_left), botutils.make_time_string(LOBBY_TIMEOUT))
            await ctx.send(msg)

        # If we are in game:
        elif globvars.master_state.session == botutils.BotState.game:
            pass
    
    @time.error
    async def time_error(self, ctx, error):
        """Error handling of the time command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
                