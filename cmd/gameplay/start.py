"""Contains the start command cog"""

import traceback
import json
import botutils
from discord.ext import commands
from ._gameplay import Gameplay
from botutils import start_votes_timer

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

error_str = language["system"]["error"]
fstart_min = language["errors"]["fstart_min"]
fstart_max = language["errors"]["fstart_max"]
start_str = language["cmd"]["start"]

class Start(Gameplay, name = language["system"]["gameplay_cog"]):
    """Start command cog"""
    
    @commands.command(
        pass_context = True,
        name = "start",
        brief = language["doc"]["start"]["brief"],
        help = language["doc"]["start"]["help"],
        description = language["doc"]["start"]["description"]
    )
    @commands.check(botutils.check_if_lobby)
    @commands.check(botutils.check_if_is_pregame_player)
    async def start(self, ctx):
        """Start command"""

        import globvars

        # The player has already voted to start
        if ctx.author.id in globvars.start_votes:
            return

        game = botutils.GameChooser().get_selected_game()

        if len(globvars.master_state.pregame) < game.MIN_PLAYERS:
            msg = fstart_min.format(
                ctx.author.mention,
                botutils.BotEmoji.cross,
                str(game),
                game.MIN_PLAYERS
            )
            await ctx.send(msg)
            return

        if len(globvars.master_state.pregame) > game.MAX_PLAYERS:
            msg = fstart_max.format(
                ctx.author.mention,
                botutils.BotEmoji.cross,
                str(game),
                game.MAX_PLAYERS
            )
            await ctx.send(msg)
            return
        
        # The player has not voted to start yet
        else:

            globvars.start_votes.append(ctx.author.id)

            # First person to vote. Start the clear start votes timer
            if len(globvars.start_votes) == 1:
                if start_votes_timer.is_running():
                    start_votes_timer.cancel()
                start_votes_timer.start()
            
            # Calculate the number of votes needed
            votes_needed = max(len(globvars.master_state.pregame) - 3, 3)

            # Reached the number of votes needed. Start the game.
            if len(globvars.start_votes) == votes_needed:
                game = botutils.GameChooser().get_selected_game()
                globvars.master_state.game = game
                await globvars.master_state.game.start_game()
                botutils.update_state_machine()

                # Clear the start votes
                globvars.start_votes.clear()
                
                return
            
            votes_left = votes_needed - len(globvars.start_votes)
            msg = start_str.format(
                ctx.author.name,
                votes_left,
                "vote" if votes_left == 1 else "votes"
            )
            await ctx.send(msg)
    
    @start.error
    async def start_error(self, ctx, error):
        """Error handling of the start command"""

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
