"""Contains the fstart command cog"""

import botutils
import json
from discord.ext import commands
from ._admin import Admin

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

fstart_min = language["errors"]["fstart_min"]
fstart_max = language["errors"]["fstart_max"]


class Fstart(Admin, name = language["system"]["admin_cog"]):
    """Fstart command"""

    @commands.command(
        pass_context = True, 
        name = "fstart",
        brief = language["doc"]["fstart"]["brief"],
        help = language["doc"]["fstart"]["help"],
        description = language["doc"]["fstart"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def fstart(self, ctx):
        """Force start command"""

        import globvars

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
            msg = fstart_min
            msg = fstart_min.format(
                ctx.author.mention,
                botutils.BotEmoji.cross,
                str(game),
                game.MAX_PLAYERS
            )
            await ctx.send(msg)
            return

        globvars.master_state.game = game
        await globvars.master_state.game.start_game()
        botutils.update_state_machine()

        # Clear the start votes
        globvars.start_votes.clear()
