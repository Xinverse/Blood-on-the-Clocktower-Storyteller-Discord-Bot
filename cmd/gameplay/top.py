"""Contains the top command cog"""

import configparser
import json
import sqlite3

import discord
from discord.ext import commands

import botutils
import globvars
from ._gameplay import Gameplay

Config = configparser.ConfigParser()
Config.read("config.INI")

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)

top_games_str = language["cmd"]["top_games"]
top_wins_str = language["cmd"]["top_wins"]
top_winrate_str = language["cmd"]["top_winrate"]
top_footer_str = language["cmd"]["top_footer"]
top_footer_winrate_str = language["cmd"]["top_footer_winrate"]


class Top(Gameplay, name = language["system"]["gameplay_cog"]):
    """Top command cog"""

    @commands.command(
        pass_context = True,
        name = "top",
        aliases = [],
        brief = language["doc"]["top"]["brief"],
        help = language["doc"]["top"]["help"],
        description = language["doc"]["top"]["description"]
    )
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def top(self, ctx, arg=None):
        """Top command"""

        msg = ""
        limit = int(Config["misc"]["TOP_LIMIT"])
        min_games = int(Config["misc"]["TOP_WINRATE_MIN_GAMES"])

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("SELECT SUM(total_games) FROM gamestats")
            total_games, = c.fetchone()

            footer = top_footer_str.format(total_games, "" if total_games == 1 else "s")

            if arg == "games":
                c = db.execute("SELECT user_id, games FROM playerstats ORDER BY games DESC")
                title = top_games_str.format(limit)
                i = 0
                last = None
                tie = 0
                for (user_id, games) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    if last is None or games < last:
                        i += 1 + tie
                        tie = 0
                    else:
                        tie += 1
                    last = games
                    if i > limit:
                        break
                    msg += f"{i}. **{discord.utils.escape_markdown(user.name)}** – {games}\n"
            elif arg == "wins":
                title = top_wins_str.format(limit)
                c = db.execute("SELECT user_id, wins FROM playerstats ORDER BY wins DESC")
                i = 0
                last = None
                tie = 0
                for (user_id, wins) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    if last is None or wins < last:
                        i += 1 + tie
                        tie = 0
                    else:
                        tie += 1
                    last = wins
                    if i > limit:
                        break
                    msg += f"{i}. **{discord.utils.escape_markdown(user.name)}** – {wins}\n"
            elif arg == "winrate":
                title = top_winrate_str.format(limit)
                footer += " · " + top_footer_winrate_str.format(min_games, "" if min_games == 1 else "s")
                c = db.execute("SELECT user_id, ((wins*1.0) / games) AS winrate FROM playerstats WHERE games >= ? ORDER BY winrate DESC", (min_games,))
                i = 0
                last = None
                tie = 0
                leaderboard = []
                for (user_id, winrate) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    if last is None or winrate < last:
                        i += 1 + tie
                        tie = 0
                    else:
                        tie += 1
                    last = winrate
                    if i > limit:
                        break
                    leaderboard.append((i, user, winrate))
                precision = 1
                while True:
                    for i in range(len(leaderboard) - 1):
                        cur_pos, _, cur_rate = leaderboard[i]
                        next_pos, _, next_rate = leaderboard[i + 1]
                        ok = True
                        if cur_pos != next_pos and cur_rate != next_rate and f"{cur_rate * 100:.{precision}f}" == f"{next_rate * 100:.{precision}f}":
                            precision += 1
                            ok = False
                            break
                    if ok:
                        break
                for (i, user, winrate) in leaderboard:
                    msg += f"{i}. **{discord.utils.escape_markdown(user.name)}** – {winrate * 100:.{precision}f}%\n"
            else:
                msg = language["cmd"]["top_usage"]
                return await ctx.send(msg)

            embed = discord.Embed(color=discord.Color.orange(), title=title, description=msg)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
