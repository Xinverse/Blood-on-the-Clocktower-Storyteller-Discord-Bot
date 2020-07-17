"""Contains the fleave command cog"""

import discord
import botutils
import json
from discord.ext import commands
from ._admin import Admin
from botutils import lobby_timeout

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

fleave_str = language["cmd"]["fleave"]
fleaved_str = language["cmd"]["fleaved"]


class Fleave(Admin, name = language["system"]["admin_cog"]):
    """Fleave command"""

    @commands.command(
        pass_context = True, 
        name = "fleave",
        brief = language["doc"]["fleave"]["brief"],
        help = language["doc"]["fleave"]["help"],
        description = language["doc"]["fleave"]["description"]
    )
    async def fleave(self, ctx, *, member: discord.Member):
        """Force leave command"""

        import globvars

        # The player has joined; make them leave.
        if globvars.master_state.pregame.is_joined(member.id):
            globvars.master_state.pregame.safe_remove_player(member.id)
            await ctx.send(fleave_str.format(member.name, len(globvars.master_state.pregame)))
            botutils.update_state_machine()
            # If you are the last player to leave, then cancel the lobby timeout loop
            if len(globvars.master_state.pregame) == 0:
                lobby_timeout.cancel()
        
        # The player has not joined.
        else:
            await ctx.send(fleaved_str.format(ctx.author.mention, member.name))

        await botutils.remove_alive_role(member)
