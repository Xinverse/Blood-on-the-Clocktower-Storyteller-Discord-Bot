"""Contains the time command"""

import traceback
import json
import botutils
from discord.ext import commands
from botc import check_if_is_player, Phase

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)
    error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)


class Time(commands.Cog, name = documentation["misc"]["townhall_cog"]):
    """BoTC in-game commands cog
    Time command - used for viewing the time left for each different phase or 
    stage of the game
    """
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check the channel of the context, return True if it is sent in 
        lobby or in spectators chat
        Admins can bypass.
        """
        return botutils.check_if_admin(ctx) or \
               check_if_is_player(ctx) or \
               botutils.check_if_spec(ctx)
    
    # ---------- TIME COMMAND ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "time", 
        aliases = ["t"], 
        hidden = False, 
        brief = documentation["doc"]["time"]["brief"],
        help = documentation["doc"]["time"]["help"],
        description = documentation["doc"]["time"]["description"]
    )
    async def time(self, ctx):
        """Time command
        usage: time
        can be used by all players or in DM
        """
        import globvars
        if globvars.master_state.game.current_phase == Phase.day:
            await ctx.send("It is currently daytime.")
        elif globvars.master_state.game.current_phase == Phase.night:
            await ctx.send("It is currently nighttime.")
        elif globvars.master_state.game.current_phase == Phase.dawn:
            await ctx.send("It is currently dawn.")

    @time.error
    async def time_error(self, ctx, error):
        # Check did not pass -> commands.CheckFailure
        if isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
