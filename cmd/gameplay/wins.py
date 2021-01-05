"""Contains the wins command cog"""

import json
import sqlite3

from discord import utils
from discord.ext import commands

import botutils
import globvars
from ._gameplay import Gameplay

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)

wins_nogames_str = language["cmd"]["wins_nogames"]
wins_str = language["cmd"]["wins"]


class Wins(Gameplay, name = language["system"]["gameplay_cog"]):
    """Wins command cog"""

    @commands.command(
        pass_context = True,
        name = "wins",
        aliases = [],
        brief = language["doc"]["wins"]["brief"],
        help = language["doc"]["wins"]["help"],
        description = language["doc"]["wins"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def wins(self, ctx, arg=None):
        """Wins command"""

        user = None

        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        elif arg:
            if arg.isnumeric():
                user = globvars.client.get_user(int(arg))
        else:
            user = ctx.author

        if not user:
            await ctx.send("User not found.")
            return

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("SELECT games, wins FROM playerstats WHERE user_id = ?", (user.id,))
            row = c.fetchone()
            print(row)

            if row:
                games, wins = row
            else:
                games, wins = 0, 0

            if games > 0:
                await ctx.send(wins_str.format(utils.escape_markdown(user.display_name), wins, games, "" if games == 1 else "s", (wins / games) * 100))
            else:
                await ctx.send(wins_nogames_str.format(utils.escape_markdown(user.display_name)))
