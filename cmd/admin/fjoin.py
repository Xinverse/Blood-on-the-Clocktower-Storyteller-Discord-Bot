"""Contains the fjoin command cog"""

import discord
import botutils
import json
from discord.ext import commands
from ._admin import Admin
from botutils import lobby_timeout

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

fjoin_str = language["cmd"]["fjoin"]
fjoined_str = language["cmd"]["fjoined"]
fjoin_max = language["errors"]["fjoin_max"]


class Fjoin(Admin, name = language["system"]["admin_cog"]):
    """Fjoin command"""

    @commands.command(
        pass_context = True,
        name = "fjoin",
        brief = language["doc"]["fjoin"]["brief"],
        help = language["doc"]["fjoin"]["help"],
        description = language["doc"]["fjoin"]["description"]
    )
    async def fjoin(self, ctx, *, member: discord.Member):
        """Force join command"""

        import globvars

        game = botutils.GameChooser().get_selected_game()

        # Too many players
        if len(globvars.master_state.pregame) >= game.MAX_PLAYERS:
            msg = fjoin_max.format(
                ctx.author.mention,
                botutils.BotEmoji.cross,
                str(game),
                game.MAX_PLAYERS
            )
            await ctx.send(msg)
            return

        # The player has already joined
        if globvars.master_state.pregame.is_joined(member.id):
            await ctx.send(fjoined_str.format(ctx.author.mention, member.name))
        
        # The player has not yet joined. Make them join.
        else:
            globvars.master_state.pregame.safe_add_player(member.id)
            botutils.update_state_machine()
            await ctx.send(fjoin_str.format(member.name, len(globvars.master_state.pregame)))
        
        # If you are the first player to join the game, then start the lobby timeout loop
        if len(globvars.master_state.pregame) == 1:
            lobby_timeout.start()

        await botutils.add_alive_role(member)
