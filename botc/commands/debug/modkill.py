"""Contains the modkill command cog"""

import json
import traceback
import botutils
from botc import PlayerConverter, PlayerNotFound, AlreadyDead
from discord.ext import commands

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    error_str = bot_text["system"]["error"]

x_emoji = botutils.BotEmoji.cross
check_emoji = botutils.BotEmoji.check


class Modkill(commands.Cog, name = documentation["misc"]["debug_cog"]):
    """Modkill command"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)

    # ---------- MODKILL command ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "modkill",
        hidden = False,
        brief = documentation["doc"]["modkill"]["brief"],
        help = documentation["doc"]["modkill"]["help"],
        description = documentation["doc"]["modkill"]["description"]
    )
    async def modkill(self, ctx, *, player: PlayerConverter()):
        """Modkill command"""
        await player.exec_real_death()
        feedback = documentation["doc"]["modkill"]["feedback"]
        await ctx.send(feedback.format(check_emoji, player.game_nametag, player.role.emoji, 
            player.role.true_self))

    @modkill.error
    async def modkill_error(self, ctx, error):
        """Modkill command error handling"""
        if isinstance(error, commands.MissingRequiredArgument):
            msg = documentation["cmd_warnings"]["missing_arguments"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, PlayerNotFound):
            msg = documentation["cmd_warnings"]["player_not_found"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, AlreadyDead):
            msg = documentation["cmd_warnings"]["already_dead"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
                