"""Contains the role command cog"""

import botutils
import json
import traceback
from discord.ext import commands
from ._gameplay import Gameplay

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]


class Role(Gameplay, name = language["system"]["gameplay_cog"]):
    """Role command cog"""

    @commands.command(
        pass_context=True, 
        name = "role", 
        aliases = ["roles", "character", 'characters'],
        brief = language["doc"]["role"]["brief"],
        help = language["doc"]["role"]["help"],
        description = language["doc"]["role"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def role(self, ctx, *, role_name):
        """Role command"""

        import globvars
        found = botutils.find_role_in_all(role_name)
        
        # We did not find the role, send them the whole list
        if found is None:
            await ctx.send(globvars.master_state.game_packs["botc"]["formatter"].create_complete_roles_list())

        # We found the role, send them that role card only
        else:
            await found.send_role_card_embed(ctx)

    @role.error
    async def role_error(self, ctx, error):
        """Error handling of the role command"""

        import globvars

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # Case: missing argument -> we will print the entire list of roles
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(globvars.master_state.game_packs["botc"]["formatter"].create_complete_roles_list())
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
