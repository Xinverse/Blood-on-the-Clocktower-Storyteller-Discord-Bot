"""Contains the coin command cog"""

import botutils
import json
import random
from ._miscellaneous import Miscellaneous
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)


class Coin(Miscellaneous, name = language["system"]["miscellaneous_cog"]):
    """Coin command"""

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
        