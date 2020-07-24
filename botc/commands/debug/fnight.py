"""Contains the fnight command cog"""

import json
import traceback
import botutils
from botc import Phase
from discord.ext import commands

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    error_str = bot_text["system"]["error"]


class Fnight(commands.Cog, name = documentation["misc"]["debug_cog"]):
    """Fnight command"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)

    # ---------- FNIGHT command ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "fnight",
        hidden = False,
        brief = documentation["doc"]["fnight"]["brief"],
        help = documentation["doc"]["fnight"]["help"],
        description = documentation["doc"]["fnight"]["description"]
    )
    async def fnight(self, ctx):
        """Fnight command"""
        
        import globvars
        if globvars.master_state.game.current_phase == Phase.day:

            from botc.gameloops import nomination_loop, base_day_loop, debate_timer

            # Stop the nomination loop if it is running
            if nomination_loop.is_running():
                nomination_loop.cancel()
            
            # Stop the base day loop if it is running
            if base_day_loop.is_running():
                base_day_loop.cancel()
            
            # Stop the debate timer loop if it is running
            if debate_timer.is_running():
                debate_timer.cancel()

            import botc.switches
            botc.switches.master_proceed_to_night = True
            msg = documentation["doc"]["fnight"]["feedback"].format(botutils.BotEmoji.success)
            
            await ctx.send(msg)
    
    @fnight.error
    async def fnight_error(self, ctx, error):
        # Check did not pass -> commands.CheckFailure
        if isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
