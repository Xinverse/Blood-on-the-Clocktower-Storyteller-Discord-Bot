"""Contains the botc debug/admin cog"""

import discord
import json
import traceback
import botutils
import globvars
from discord.ext import commands
from botc import PlayerConverter, PlayerNotFound, RoleConverter, RoleNotFound

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    check_emoji = bot_text["esthetics"]["check_emoji"]
    error_str = bot_text["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)


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
        player.exec_change_role(role)
        player.role.exec_init_role(globvars.master_state.game.setup)
        try:
            await player.role.ego_self.send_opening_dm_embed(player.user)
        except discord.Forbidden:
            pass
        await ctx.send(f"{check_emoji} Successfully changed {player.game_nametag}'s role to `{role}`.")

    @frole.error
    async def frole_error(self, ctx, error):
        """Frole command error handling"""
        if isinstance(error, commands.MissingRequiredArgument):
            pass
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
    async def modkill(self, ctx, player: PlayerConverter()):
        """Modkill command"""
        await player.exec_real_death()
        await ctx.send(f"{check_emoji} Successfully modkilled {player.game_nametag}.")

    @modkill.error
    async def modkill_error(self, ctx, error):
        """Modkill command error handling"""
        try:
            raise error
        except:
            await ctx.send(error_str)
            await botutils.log(botutils.Level.error, traceback.format_exc())


def setup(client):
    client.add_cog(BoTCDebugCommands(client))
