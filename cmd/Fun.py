"""Contains the Fun cog: fun related commands"""

import botutils
import random
import traceback
import json
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

dog_str = language["cmd"]["dog"]


class Fun(commands.Cog, name="Fun Commands"):
    """Fun cog"""
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_not_ignored(ctx)

    # ---------- DOG COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "dog")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def dog(self, ctx):
        """Flip a dog."""

        await ctx.send(dog_str)
    

    async def cog_command_error(self, ctx, error):
        """Error handling on commands"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await botutils.log(self.client, botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Fun(client))
