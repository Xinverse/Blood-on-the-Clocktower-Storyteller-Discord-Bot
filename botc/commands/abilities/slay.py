"""Slay command"""

import botutils
import discord
import traceback
import json
from discord.ext import commands
from botc import check_if_is_player, check_if_is_day, check_if_lobby, RoleCannotUseCommand, \
    check_if_player_really_alive, check_if_can_slay, PlayerParser, AbilityForbidden, \
    NotAPlayer, BOTCUtils, AliveOnlyCommand, NotDay, NotLobbyChannel

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)


class Slay(commands.Cog, name = "༺ 𝕭𝖑𝖔𝖔𝖉 𝖔𝖓 𝖙𝖍𝖊 𝕮𝖑𝖔𝖈𝖐𝖙𝖔𝖜𝖊𝖗 ༻ 𝔄𝔟𝔦𝔩𝔦𝔱𝔦𝔢𝔰"):
    """BoTC in-game commands cog
    Slay command - used by slayer
    """
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check performed on all commands of this cog.
        Must be a non-fleaved player to use these commands.
        """
        return check_if_is_player(ctx)  # Registered non-quit player -> NotAPlayer
    
    # ---------- SLAY COMMAND (Slayer) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "slay",
        hidden = True,
        brief = documentation["doc"]["slay"]["brief"],
        help = documentation["doc"]["slay"]["help"],
        description = documentation["doc"]["slay"]["description"]
    )
    @commands.check(check_if_lobby)  # Correct channel -> NotLobbyChannel
    @commands.check(check_if_is_day)  # Correct phase -> NotDay
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    @commands.check(check_if_can_slay)  # Correct character -> RoleCannotUseCommand
    async def slay(self, ctx, *, slain: PlayerParser()):
        """Slay command
        usage: slay <player> and <player> and...
        characters: slayer
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.register_slay(player, slain)

    @slay.error
    async def slay_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # If it passed all the checks but raised an error in the character class
        elif isinstance(error, AbilityForbidden):
            error = getattr(error, 'original', error)
            await ctx.author.send(error)
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect argument -> commands.BadArgument
        elif isinstance(error, commands.BadArgument):
            return
        # Incorrect channel -> NotLobbyChannel
        elif isinstance(error, NotLobbyChannel):
            try:
                await ctx.author.send(documentation["cmd_warnings"]["lobby_only"].format(ctx.author.mention, emoji))
            except discord.Forbidden:
                pass
        # Incorrect phase -> NotDay
        elif isinstance(error, NotDay):
            try:
                await ctx.author.send(documentation["cmd_warnings"]["day_only"].format(ctx.author.mention, emoji))
            except discord.Forbidden:
                pass
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            try:
                await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
            except discord.Forbidden:
                pass
        # Missing argument -> commands.MissingRequiredArgument
        elif isinstance(error, commands.MissingRequiredArgument):
            from botc.gamemodes.troublebrewing import Slayer
            msg = Slayer().emoji + " " + Slayer().instruction + " " + Slayer().action
            await ctx.send(msg)
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Slay(client))
    