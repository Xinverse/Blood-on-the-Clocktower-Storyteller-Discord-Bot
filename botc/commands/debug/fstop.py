"""Contains the fstop command cog"""

import json
import traceback
import botutils
from discord.ext import commands

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    error_str = bot_text["system"]["error"]


class Fstop(commands.Cog, name = documentation["misc"]["debug_cog"]):
    """Fstop command"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)

    # ---------- FSTOP command ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "fstop",
        hidden = False,
        brief = documentation["doc"]["fstop"]["brief"],
        help = documentation["doc"]["fstop"]["help"],
        description = documentation["doc"]["fstop"]["description"]
    )
    async def fstop(self, ctx):
        """Fstop command"""

        from botc.gameloops import nomination_loop, base_day_loop

        # Stop the nomination loop if it is running
        if nomination_loop.is_running():
            nomination_loop.cancel()
        
        # Stop the base day loop if it is running
        if base_day_loop.is_running():
            base_day_loop.cancel()
        
        # Stop the gameplay loop if it is running
        import globvars
        if globvars.master_state.game.gameloop.is_running():
            globvars.master_state.game.gameloop.cancel()
            feedback = documentation["doc"]["fstop"]["feedback"]
            await ctx.send(feedback.format(botutils.BotEmoji.check))
        else:
            feedback = documentation["cmd_warnings"]["no_game_running"]
            await ctx.send(feedback.format(ctx.author.mention, botutils.BotEmoji.cross))

    @fstop.error
    async def fstop_error(self, ctx, error):
        """Fstop command error handling"""
        if isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
