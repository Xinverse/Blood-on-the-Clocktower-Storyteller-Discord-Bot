"""Contains the playerstats command cog"""

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

playerstats_title_str = language["cmd"]["playerstats_title"]
playerstats_games_str = language["cmd"]["playerstats_games"]
playerstats_wins_str = language["cmd"]["playerstats_wins"]
playerstats_winrate_str = language["cmd"]["playerstats_winrate"]
playerstats_good_games_str = language["cmd"]["playerstats_good_games"]
playerstats_good_wins_str = language["cmd"]["playerstats_good_wins"]
playerstats_good_winrate_str = language["cmd"]["playerstats_good_winrate"]
playerstats_evil_games_str = language["cmd"]["playerstats_evil_games"]
playerstats_evil_wins_str = language["cmd"]["playerstats_evil_wins"]
playerstats_evil_winrate_str = language["cmd"]["playerstats_evil_winrate"]
playerstats_footer_str = language["cmd"]["playerstats_footer"]
user_not_found_str = language["errors"]["user_not_found"]
error_str = language["system"]["error"]


class Playerstats(Gameplay, name = language["system"]["gameplay_cog"]):
    """Playerstats command cog"""

    @commands.command(
        pass_context = True,
        name = "playerstats",
        aliases = ["games", "wins"],
        brief = language["doc"]["playerstats"]["brief"],
        help = language["doc"]["playerstats"]["help"],
        description = language["doc"]["playerstats"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def playerstats(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Playerstats command"""

        if not user:
            user = ctx.author

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("SELECT total_games FROM gamestats")
            total_games, = c.fetchone()

            c = db.execute("SELECT games, wins, good_games, good_wins, evil_games, evil_wins FROM playerstats WHERE user_id = ?", (user.id,))
            row = c.fetchone()
            print(row)

            if row:
                games, wins, good_games, good_wins, evil_games, evil_wins = row
            else:
                games, wins, good_games, good_wins, evil_games, evil_wins = 0, 0, 0, 0, 0, 0

            if games > 0:
                winrate = f"{(wins / games) * 100:.1f}%"
            else:
                winrate = "N/A"

            if good_games > 0:
                good_winrate = f"{(good_wins / good_games) * 100:.1f}%"
            else:
                good_winrate = "N/A"

            if evil_games > 0:
                evil_winrate = f"{(evil_wins / evil_games) * 100:.1f}%"
            else:
                evil_winrate = "N/A"

            embed = discord.Embed(color=discord.Color.green(), title=playerstats_title_str)
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.add_field(name=playerstats_games_str, value=str(games), inline=True)
            embed.add_field(name=playerstats_wins_str, value=str(wins), inline=True)
            embed.add_field(name=playerstats_winrate_str, value=str(winrate) + '\n\u200b', inline=True)
            embed.add_field(name=playerstats_good_games_str, value=str(good_games), inline=True)
            embed.add_field(name=playerstats_good_wins_str, value=str(good_wins), inline=True)
            embed.add_field(name=playerstats_good_winrate_str, value=str(good_winrate) + '\n\u200b', inline=True)
            embed.add_field(name=playerstats_evil_games_str, value=str(evil_games), inline=True)
            embed.add_field(name=playerstats_evil_wins_str, value=str(evil_wins), inline=True)
            embed.add_field(name=playerstats_evil_winrate_str, value=str(evil_winrate), inline=True)
            embed.set_footer(text=playerstats_footer_str.format(total_games, "" if total_games == 1 else "s"))
            await ctx.send(embed=embed)

    @playerstats.error
    async def playerstats_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send(user_not_found_str.format(ctx.author.mention))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())
