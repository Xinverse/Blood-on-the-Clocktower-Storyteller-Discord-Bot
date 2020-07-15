"""Contains the botc debug/admin cog"""

import discord
import json
import traceback
import botutils
import globvars
from discord.ext import commands
from botc import PlayerConverter, PlayerNotFound, RoleConverter, RoleNotFound, AlreadyDead

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    check_emoji = bot_text["esthetics"]["check_emoji"]
    error_str = bot_text["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    x_emoji = documentation["cmd_warnings"]["x_emoji"]


class BoTCDebugCommands(commands.Cog, name = "BoTC debug commands"):
    """BoTC in-game debug commands cog"""

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
        old_role = player.role.true_self
        await player.exec_change_role(role)
        player.role.exec_init_role(globvars.master_state.game.setup)
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


def setup(client):
    client.add_cog(BoTCDebugCommands(client))
