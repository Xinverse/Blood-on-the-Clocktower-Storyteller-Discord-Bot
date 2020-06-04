"""Contains the Fun cog: fun related commands"""

import botutils
import random
import traceback
import json
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

class Fun(commands.Cog, name="Fun Commands"):
    """Fun cog"""
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_not_ignored(ctx)

    # ---------- DOG COMMAND ----------------------------------------

    @commands.command(
        pass_context=True, 
        name = "dog", 
        brief = language["doc"]["dog"]["brief"],
        help = language["doc"]["dog"]["help"],
        description = language["doc"]["dog"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def dog(self, ctx):
        """Flip a dog."""

        dog_replies = language["doc"]["dog"]["outputs"]
        dog_weights = language["doc"]["dog"]["weights"]
        dog_reply = random.choices(
            dog_replies, 
            weights=dog_weights
        )
        dog_reply = dog_reply[0]

        await ctx.send(dog_reply)
    
    # ---------- COIN COMMAND ----------------------------------------

    @commands.command(
        pass_context=True, 
        name = "coin", 
        brief = language["doc"]["coin"]["brief"],
        help = language["doc"]["coin"]["help"],
        description = language["doc"]["coin"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def coin(self, ctx):
        """Flip a coin."""

        coin_replies = language["doc"]["coin"]["outputs"]
        coin_weights = language["doc"]["coin"]["weights"]
        coin_reply = random.choices(
            coin_replies,
            weights=coin_weights
        )
        coin_reply = coin_reply[0]

        await ctx.send(coin_reply)
    

    # -------------------------------------------------------

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
    client.add_cog(Fun(client))
