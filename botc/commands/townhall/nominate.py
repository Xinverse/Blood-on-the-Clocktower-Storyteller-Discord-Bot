"""Nominate command"""

import traceback
import json
import botutils
from discord.ext import commands
from botc import check_if_is_player, check_if_lobby, check_if_player_apparently_alive, \
    check_if_is_day, PlayerConverter, BOTCUtils, NotAPlayer, NotDay, NotLobbyChannel, \
    AliveOnlyCommand

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)


class Nominate(commands.Cog, name = "༺ 𝕭𝖑𝖔𝖔𝖉 𝖔𝖓 𝖙𝖍𝖊 𝕮𝖑𝖔𝖈𝖐𝖙𝖔𝖜𝖊𝖗 ༻ 𝔱𝔬𝔴𝔫𝔥𝔞𝔩𝔩"):
    """BoTC in-game commands cog
    Nominate command - used for execution
    """
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check performed on all commands of this cog.
        Must be a non-fleaved player to use these commands.
        """
        return check_if_is_player(ctx)  # Registered non-quit player -> NotAPlayer
    
    # ---------- NOMINATE COMMAND (Voting) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "nominate", 
        hidden = False, 
        brief = documentation["doc"]["nominate"]["brief"],
        help = documentation["doc"]["nominate"]["help"],
        description = documentation["doc"]["nominate"]["description"]
    )
    @commands.check(check_if_lobby)  # Correct channel -> NotLobbyChannel
    @commands.check(check_if_is_day)  # Correct phase -> NotDay
    @commands.check(check_if_player_apparently_alive)  # Player alive -> AliveOnlyCommand
    async def nominate(self, ctx, *, nominated: PlayerConverter()):
        """Nominate command
        usage: nominate <player> 
        characters: living players
        """
        import globvars
        from botc.gameloops import nomination_loop
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await nomination_loop(globvars.master_state.game, player, nominated)

    @nominate.error
    async def nominate_error(self, ctx, error):
        emoji = botutils.BotEmoji.cross
        # Non-registered or quit player -> NotAPlayer
        if isinstance(error, NotAPlayer):
            return
        # Incorrect argument -> commands.BadArgument
        elif isinstance(error, commands.BadArgument):
            await ctx.send(documentation["cmd_warnings"]["player_not_found"].format(ctx.author.mention, emoji))
        # Incorrect channel -> NotLobbyChannel
        elif isinstance(error, NotLobbyChannel):
            await ctx.send(documentation["cmd_warnings"]["lobby_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        # Incorrect phase -> NotDay
        elif isinstance(error, NotDay):
            await ctx.send(documentation["cmd_warnings"]["day_only"].format(ctx.author.mention, emoji))
        # Missing argument -> commands.MissingRequiredArgument
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(documentation["cmd_warnings"]["player_not_found"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 

def setup(client):
    client.add_cog(Nominate(client))
    