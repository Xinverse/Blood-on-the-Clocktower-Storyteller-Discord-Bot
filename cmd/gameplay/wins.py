"""Contains the wins command cog"""

import json
import sqlite3
import traceback
from typing import Union

import discord
from discord.ext import commands

import botutils
from ._gameplay import Gameplay

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)

wins_str = language["cmd"]["wins"]
wins_nogames_str = language["cmd"]["wins_nogames"]
user_not_found_str = language["errors"]["user_not_found"]
error_str = language["system"]["error"]


class Wins(Gameplay, name = language["system"]["gameplay_cog"]):
    """Wins command cog"""

    @commands.command(
        pass_context = True,
        name = "wins",
        aliases = ["games"],
        brief = language["doc"]["wins"]["brief"],
        help = language["doc"]["wins"]["help"],
        description = language["doc"]["wins"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def wins(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Wins command"""

        if not user:
            user = ctx.author

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("SELECT games, wins FROM playerstats WHERE user_id = ?", (user.id,))
            row = c.fetchone()
            print(row)

            if row:
                games, wins = row
            else:
                games, wins = 0, 0

            if games > 0:
                await ctx.send(wins_str.format(discord.utils.escape_markdown(user.name), wins, games, "" if games == 1 else "s", (wins / games) * 100))
            else:
                await ctx.send(wins_nogames_str.format(discord.utils.escape_markdown(user.name)))

    @wins.error
    async def wins_error(self, ctx, error):
        if isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send(user_not_found_str.format(ctx.author.mention))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
