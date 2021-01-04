"""Contains the quit command cog"""

import botutils
import traceback
import json
from discord.ext import commands
from ._gameplay import Gameplay
from botutils import lobby_timeout, start_votes_timer

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]
error_str = language["system"]["error"]


class Quit(Gameplay, name = language["system"]["gameplay_cog"]):
    """Quit command cog"""

    @commands.command(
        pass_context = True,
        name = "quit",
        aliases = ["q", "leave"],
        brief = language["doc"]["quit"]["brief"],
        help = language["doc"]["quit"]["help"],
        description = language["doc"]["quit"]["description"]
    )
    @commands.check(botutils.check_if_lobby)
    async def quit(self, ctx):
        """Quit command"""

        import globvars

        if globvars.master_state.game:
            # This check is to ensure a player doesn't quit right after !start
            # before the game is fully set up and end up breaking the game.
            return
        
        # The command user has joined; make them quit
        if globvars.master_state.pregame.is_joined(ctx.author.id):
            globvars.master_state.pregame.safe_remove_player(ctx.author.id)
            botutils.update_state_machine()
            await ctx.send(quit_str.format(ctx.author.name, len(globvars.master_state.pregame)))
            # If you are the last player to leave, then cancel the lobby timeout loop
            if len(globvars.master_state.pregame) == 0:
                lobby_timeout.cancel()
            # If the player has voted to start, then remove the start vote
            if ctx.author.id in globvars.start_votes:
                globvars.start_votes.remove(ctx.author.id)
            # Cancel the start clear timer if no one has voted to start
            if len(globvars.start_votes) == 0 and start_votes_timer.is_running():
                start_votes_timer.cancel()

        # The command user has not joined
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        
        # Still take away the role from everyone just in case of discord sync issue
        await botutils.remove_alive_role(ctx.author, unlock=True)
    
    @quit.error
    async def quit_error(self, ctx, error):
        """Error handling of the quit command"""

        # Case: check failure
        if isinstance(error, commands.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
