"""Contains the stats command cog"""

import botutils
import json
import configparser
import traceback
from discord.ext import commands
from ._gameplay import Gameplay

Config = configparser.ConfigParser()
Config.read("config.INI")

PREFIX = Config["settings"]["PREFIX"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]
no_game = language["cmd"]["no_game"]


class Stats(Gameplay, name = language["system"]["gameplay_cog"]):
    """Stats command"""

    @commands.command(
        pass_context = True, 
        name = "stats", 
        aliases = ["statistics"],
        brief = language["doc"]["stats"]["brief"],
        help = language["doc"]["stats"]["help"],
        description = language["doc"]["stats"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_spec_or_dm_or_admin)
    async def stats(self, ctx):
        """Stats command"""

        import globvars

        # If we are in pregame:
        if globvars.master_state.session == botutils.BotState.pregame:
            await botutils.send_pregame_stats(ctx, globvars.master_state.pregame.list)

        # If we are in game:
        elif globvars.master_state.session == botutils.BotState.game:
            return
        
        # If we are in empty
        elif globvars.master_state.session == botutils.BotState.empty:
            await ctx.send(no_game.format(PREFIX))
    
    @stats.error
    async def stats_error(self, ctx, error):
        """Error handling of the stats command"""

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
