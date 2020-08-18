"""Contains the deop command cog"""

import botutils
import json
from discord.ext import commands
from ._admin import Admin

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)


class Deop(Admin, name = language["system"]["admin_cog"]):
    """Deop command"""

    @commands.command(
        pass_context = True,
        name = "deop",
        aliases = ["fdeop"],
        brief = language["doc"]["deop"]["brief"],
        help = language["doc"]["deop"]["help"],
        description = language["doc"]["deop"]["description"]
    )
    async def deop(self, ctx):
        """Remove the admin role from the user"""
        await botutils.remove_admin_role(ctx.author)
        await ctx.send(f"{ctx.author.mention} {botutils.BotEmoji.success}")

