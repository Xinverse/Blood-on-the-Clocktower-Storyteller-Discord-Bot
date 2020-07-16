"""Contains the op command cog"""

import botutils
import json
from discord.ext import commands
from ._admin import Admin

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)


class Op(Admin, name = "༺ 𝕬𝖉𝖒𝖎𝖓𝖎𝖘𝖙𝖗𝖆𝖙𝖔𝖗 ༻"):
    """Op command"""

    @commands.command(
        pass_context=True, 
        name = "op",
        aliases = ["fop"],
        brief = language["doc"]["op"]["brief"],
        help = language["doc"]["op"]["help"],
        description = language["doc"]["op"]["description"]
    )
    async def op(self, ctx):
        """Give the admin role to the user"""
        await botutils.add_admin_role(ctx.author)
        await ctx.send(f"{ctx.author.mention} {botutils.BotEmoji.success}")
