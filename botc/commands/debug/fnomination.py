"""Contains the fnomination command cog"""

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


class Fnomination(commands.Cog, name = documentation["misc"]["debug_cog"]):
    """Fnomination command"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)

    # ---------- FNOMINATION command ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "fnomination",
        hidden = False,
        brief = documentation["doc"]["fnomination"]["brief"],
        help = documentation["doc"]["fnomination"]["help"],
        description = documentation["doc"]["fnomination"]["description"]
    )
    async def fnomination(self, ctx):
        """fnomination command"""
        
        import globvars
        if globvars.master_state.game.current_phase == Phase.day:
            from botc.gameloops import base_day_loop
            if base_day_loop.is_running():
                base_day_loop.cancel()
                import botc.switches
                botc.switches.master_proceed_to_nomination = True
                msg = documentation["doc"]["fnomination"]["feedback"].format(botutils.BotEmoji.success)
                await ctx.send(msg)
    
    @fnomination.error
    async def fnomination_error(self, ctx, error):
        # Check did not pass -> commands.CheckFailure
        if isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
