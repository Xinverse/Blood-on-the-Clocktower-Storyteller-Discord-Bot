"""Contains the dog command cog"""

import botutils
import random
import json
from ._miscellaneous import Miscellaneous
from discord.ext import commands

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)


class Dog(Miscellaneous, name = language["system"]["miscellaneous_cog"]):
    """Dog command"""

    @commands.command(
        pass_context = True,
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
        dog_reply = dog_reply.format(botutils.BotEmoji.puppy)

        await ctx.send(dog_reply)
