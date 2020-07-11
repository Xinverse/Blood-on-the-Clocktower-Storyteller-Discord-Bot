"""Contains the Owner only cog"""

import botutils
import traceback
import json
import globvars
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]


class Owner(commands.Cog, name="Owner-only Commands"):
    """Owner commands cog"""
    
    def __init__(self, client):
        self.client = client

    @commands.command(
        pass_context = True,
        name = "eval"
    )
    @commands.is_owner()
    async def cmd_eval(self, ctx, *, expression):
        await ctx.send(botutils.make_code_block(eval(expression)))

    async def cog_command_error(self, ctx, error):
        """Error handling on commands"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Owner(client))
