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
gamestats_title_players_str = language["cmd"]["gamestats_title_players"]
gamestats_total_games_str = language["cmd"]["gamestats_total_games"]
gamestats_good_wins_str = language["cmd"]["gamestats_good_wins"]
gamestats_evil_wins_str = language["cmd"]["gamestats_evil_wins"]
error_title_str = language["errors"]["error_title"]
gamestats_invalid_str = language["cmd"]["gamestats_invalid"]
gamestats_no_games_str = language["cmd"]["gamestats_no_games"]


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
    async def gamestats(self, ctx, players: int = None):
        """Gamestats command"""

        with sqlite3.connect("data.sqlite3") as db:
            if players:
                c = db.execute("SELECT total_games, good_wins, evil_wins FROM gamestats WHERE players = ?", (players,))
                title = gamestats_title_players_str.format(players)
            else:
                c = db.execute("SELECT SUM(total_games), SUM(good_wins), SUM(evil_wins) FROM gamestats")
                title = gamestats_title_str

            row = c.fetchone()
            if not row:
                return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title=error_title_str, description=gamestats_invalid_str))

            total_games, good_wins, evil_wins = row
            if not total_games:
                return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title=error_title_str, description=gamestats_no_games_str))

            embed = discord.Embed(color=discord.Color.blue(), title=title)
            embed.add_field(name=gamestats_total_games_str, value=str(total_games), inline=True)
            embed.add_field(name=gamestats_good_wins_str, value=f"{good_wins} ({(good_wins / total_games) * 100:.1f}%)", inline=True)
            embed.add_field(name=gamestats_evil_wins_str, value=f"{evil_wins} ({(evil_wins / total_games) * 100:.1f}%)", inline=True)
            await ctx.send(embed=embed)
