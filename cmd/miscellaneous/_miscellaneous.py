"""Contains miscellaneous commands"""

import json
import botutils
import traceback
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]


class Miscellaneous(commands.Cog, name = language["system"]["miscellaneous_cog"]):
    """Miscellaneous commands cog"""

    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return botutils.check_if_not_ignored(ctx)
    
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
