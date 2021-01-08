"""Contains the frestart command cog"""

import json
import os
import sys

from discord.ext import commands

import botutils
import globvars

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)


class Frestart(commands.Cog, name = language["system"]["admin_cog"]):
    """Frestart command"""

    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)

    # ---------- FRESTART command ----------------------------------------
    @commands.command(
        pass_context = True,
        name = "frestart",
        hidden = False,
        brief = language["doc"]["frestart"]["frestart"]["brief"],
        help = language["doc"]["frestart"]["frestart"]["help"],
        description = language["doc"]["frestart"]["frestart"]["description"]
    )
    async def frestart(self, ctx, arg=None):
        """Frestart command"""

        if globvars.master_state.game and arg != "--force":
            await ctx.send(language["cmd"]["frestart_confirm"].format(ctx.author.mention, botutils.BotEmoji.cross))
            return

        await ctx.send(language["cmd"]["frestart"].format(ctx.author.mention, botutils.BotEmoji.success))
        os.execl(sys.executable, sys.executable, *sys.argv)
