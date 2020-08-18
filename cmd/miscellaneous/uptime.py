"""Contains the uptime command cog"""

import botutils
import json
from time import time
from discord.ext import commands
from datetime import timedelta
from ._miscellaneous import Miscellaneous

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

uptime_str = language["cmd"]["uptime"]


class Uptime(Miscellaneous, name = language["system"]["miscellaneous_cog"]):
    """Uptime command"""

    @commands.command(
        pass_context = True,
        name = "uptime",
        brief = language["doc"]["uptime"]["brief"],
        help = language["doc"]["uptime"]["help"],
        description = language["doc"]["uptime"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def uptime(self, ctx):
        """Check the uptime."""

        import globvars
        uptime = time() - globvars.master_state.boottime
        uptime = round(uptime)
        uptime_formatted = str(timedelta(seconds=uptime))
        msg = uptime_str.format(botutils.BotEmoji.alarmclock, uptime_formatted)
        await ctx.send(msg)
