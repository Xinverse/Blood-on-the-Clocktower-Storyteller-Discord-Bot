"""Contains the gamestats command cog"""

import json
import sqlite3

import discord
from discord.ext import commands

import botutils
from ._gameplay import Gameplay

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)

gamestats_title_str = language["cmd"]["gamestats_title"]
gamestats_total_games_str = language["cmd"]["gamestats_total_games"]
gamestats_good_wins_str = language["cmd"]["gamestats_good_wins"]
gamestats_evil_wins_str = language["cmd"]["gamestats_evil_wins"]


class Gamestats(Gameplay, name = language["system"]["gameplay_cog"]):
    """Gamestats command cog"""

    @commands.command(
        pass_context = True,
        name = "gamestats",
        brief = language["doc"]["gamestats"]["brief"],
        help = language["doc"]["gamestats"]["help"],
        description = language["doc"]["gamestats"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def gamestats(self, ctx):
        """Gamestats command"""

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("SELECT total_games, good_wins, evil_wins FROM gamestats")
            total_games, good_wins, evil_wins = c.fetchone()

            embed = discord.Embed(color=discord.Color.blue(), title=gamestats_title_str)
            embed.add_field(name=gamestats_total_games_str, value=str(total_games), inline=True)
            embed.add_field(name=gamestats_good_wins_str, value=f"{good_wins} ({(good_wins / total_games) * 100:.1f}%)", inline=True)
            embed.add_field(name=gamestats_evil_wins_str, value=f"{evil_wins} ({(evil_wins / total_games) * 100:.1f}%)", inline=True)
            await ctx.send(embed=embed)
