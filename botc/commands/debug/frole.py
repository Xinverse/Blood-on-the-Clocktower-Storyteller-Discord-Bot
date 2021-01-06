"""Contains the frole command cog"""

import json
import traceback
import botutils
import discord
from discord.ext import commands
from botc import PlayerConverter, RoleConverter, PlayerNotFound, RoleNotFound

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    error_str = bot_text["system"]["error"]

x_emoji = botutils.BotEmoji.cross
check_emoji = botutils.BotEmoji.check


class Frole(commands.Cog, name = documentation["misc"]["debug_cog"]):
    """Frole command"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)
    
    # ---------- FROLE command ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "frole",
        hidden = False,
        brief = documentation["doc"]["frole"]["brief"],
        help = documentation["doc"]["frole"]["help"],
        description = documentation["doc"]["frole"]["description"]
    )
    async def frole(self, ctx, player: PlayerConverter(), role: RoleConverter()):
        """Frole command"""
        import globvars
        old_role = player.role.true_self
        await player.exec_change_role(role)
        player.role.exec_init_role(globvars.master_state.game.setup)
        globvars.master_state.game.invalidated = True
        try:
            await player.role.ego_self.send_opening_dm_embed(player.user)
        except discord.Forbidden:
            pass
        feedback = documentation["doc"]["frole"]["feedback"]
        await ctx.send(feedback.format(check_emoji, player.game_nametag, old_role, role.emoji, role))

    @frole.error
    async def frole_error(self, ctx, error):
        """Frole command error handling"""
        if isinstance(error, commands.MissingRequiredArgument):
            msg = documentation["cmd_warnings"]["missing_arguments"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, PlayerNotFound):
            msg = documentation["cmd_warnings"]["player_not_found"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, RoleNotFound):
            msg = documentation["cmd_warnings"]["role_not_found"]
            await ctx.send(msg.format(ctx.author.mention, x_emoji))
        elif isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
                