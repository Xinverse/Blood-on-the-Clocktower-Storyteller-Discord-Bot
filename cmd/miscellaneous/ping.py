"""Contains the ping command cog"""

import botutils
import json
from discord.ext import commands
from ._miscellaneous import Miscellaneous

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

ping_str = language["cmd"]["ping"]


class Ping(Miscellaneous, name = language["system"]["miscellaneous_cog"]):
    """Ping command"""

    @commands.command(
        pass_context = True,
        name = "ping",
        aliases = ["pong"],
        brief = language["doc"]["ping"]["brief"],
        help = language["doc"]["ping"]["help"],
        description = language["doc"]["ping"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def ping(self, ctx):
        """Check the latency."""
        msg = ping_str.format(botutils.BotEmoji.beating_heart, round(self.client.latency, 4))
        await ctx.send(msg)
