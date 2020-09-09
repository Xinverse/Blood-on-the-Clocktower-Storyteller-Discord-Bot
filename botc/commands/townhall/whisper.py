"""Whisper command cog"""

import botutils
import traceback
import discord
import json
import asyncio
import configparser
from discord.ext import commands
from botc import check_if_is_player, check_if_dm, check_if_is_day, PlayerConverter, \
    NotDMChannel, NotAPlayer, NotDay, WhisperConverter, WhisperTooLong, BOTCUtils

Config = configparser.ConfigParser()
Config.read("preferences.INI")

WHISPER_COOLDOWN = Config["botc"]["WHISPER_COOLDOWN"]
WHISPER_COOLDOWN = int(WHISPER_COOLDOWN)
WHISPER_SHOW_TIME = Config["botc"]["WHISPER_SHOW_TIME"]
WHISPER_SHOW_TIME = int(WHISPER_SHOW_TIME)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    cooldown = documentation["cmd_warnings"]["cooldown"]
    recipient_blocked = documentation["cmd_warnings"]["recipient_blocked"]
    whisper_announcement = documentation["gameplay"]["whisper_announcement"]
    from_str = documentation["gameplay"]["from"]
    to_str = documentation["gameplay"]["to"]
    whisper_self = documentation["cmd_warnings"]["whisper_self"]


class Whisper(commands.Cog, name = documentation["misc"]["townhall_cog"]):
    """Whisper command"""
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check performed on all commands of this cog.
        Must be a non-fleaved player to use these commands.
        """
        return check_if_is_player(ctx)  # Registered non-quit player -> NotAPlayer
    
    # ---------- WHISPER COMMAND ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "whisper",
        aliases = ["w"],
        hidden = False, 
        cooldown_after_parsing = True, 
        brief = documentation["doc"]["whisper"]["brief"],
        help = documentation["doc"]["whisper"]["help"],
        description = documentation["doc"]["whisper"]["description"]
    )
    @commands.cooldown(1, WHISPER_COOLDOWN, commands.BucketType.channel)
    @commands.check(check_if_is_day)  # Correct phase -> NotDay
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    async def whisper(self, ctx, recipient: PlayerConverter(), *, content: WhisperConverter()):
        """Whisper command"""
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        # You may not whisper to yourself
        if player.user.id == recipient.user.id:
            msg = whisper_self.format(
                botutils.BotEmoji.cross,
                ctx.author.mention
            )
            try:
                await ctx.author.send(msg)
            except discord.Forbidden:
                pass
            return
        try:
            msg = from_str.format(
                botutils.BotEmoji.unread_message,
                player.game_nametag,
                content
            )
            await recipient.user.send(msg)
        except discord.Forbidden:
            msg = recipient_blocked.format(botutils.BotEmoji.warning_sign)
            await ctx.send(msg)
        else:
            msg = to_str.format(
                botutils.BotEmoji.whisper,
                recipient.game_nametag,
                content
            )
            await ctx.send(msg)
            announcement_msg = whisper_announcement.format(
                botutils.BotEmoji.opened_letter,
                player.game_nametag,
                recipient.game_nametag,
            )
            lobby_message = await botutils.send_lobby(announcement_msg)
            await asyncio.sleep(WHISPER_SHOW_TIME)
            await lobby_message.delete()
            
    @whisper.error
    async def whisper_error(self, ctx, error):
        emoji = botutils.BotEmoji.cross
        # Non-registered or quit player -> NotAPlayer
        if isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Command on cooldown -> commands.CommandOnCooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(cooldown.format(ctx.author.mention, emoji))
        # Incorrect argument -> commands.BadArgument
        elif isinstance(error, commands.BadArgument):
            await ctx.send(documentation["cmd_warnings"]["player_not_found"].format(ctx.author.mention, emoji))
        # Incorrect phase -> NotDay
        elif isinstance(error, NotDay):
            await ctx.send(documentation["cmd_warnings"]["day_only"].format(ctx.author.mention, emoji))
        # Missing argument -> commands.MissingRequiredArgument
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(documentation["cmd_warnings"]["player_not_found"].format(ctx.author.mention, emoji))
        # Whisper too long -> WhisperTooLong
        elif isinstance(error, WhisperTooLong):
            await ctx.send(documentation["cmd_warnings"]["whisper_too_long"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Whisper(client))
