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
            import botc.switches
            botc.switches.master_proceed_to_night = True
            msg = documentation["doc"]["fnight"]["feedback"].format(botutils.BotEmoji.success)
            await ctx.send(msg)
