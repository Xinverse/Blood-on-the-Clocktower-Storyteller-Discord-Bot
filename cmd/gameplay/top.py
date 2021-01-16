"""Contains the top command cog"""

import configparser
import json
import sqlite3

from discord import utils
from discord.ext import commands

import botutils
import globvars
from ._gameplay import Gameplay

Config = configparser.ConfigParser()
Config.read("config.INI")

with open("botutils/bot_text.json") as json_file:
    language = json.load(json_file)


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
            if arg == "games":
                c = db.execute("SELECT user_id, games FROM playerstats ORDER BY games DESC")
                msg = f"__Top {limit} by games played__\n\n"
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
                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {games}\n"
                    if i >= limit:
                        break
            elif arg == "wins":
                msg = f"__Top {limit} by games won__\n\n"
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

                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {wins}\n"
                    if i >= limit:
                        break
            elif arg == "winrate":
                msg = f"__Top {limit} by win rate__ (minimum {min_games} games)\n\n"
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
                    leaderboard.append((i, user, winrate))
                    if i >= limit:
                        break
                precision = 0
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
                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {winrate * 100:.{precision}f}%\n"
            else:
                msg = language["cmd"]["top_usage"]

        await ctx.send(msg)
