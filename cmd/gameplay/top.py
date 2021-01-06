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
                for (user_id, games) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    i += 1
                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {games}\n"
                    if i >= limit:
                        break
            elif arg == "wins":
                msg = f"__Top {limit} by games won__\n\n"
                c = db.execute("SELECT user_id, wins FROM playerstats ORDER BY wins DESC")
                i = 0
                for (user_id, wins) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    i += 1
                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {wins}\n"
                    if i >= limit:
                        break
            elif arg == "winrate":
                msg = f"__Top {limit} by win rate__ (minimum {min_games} games)\n\n"
                c = db.execute("SELECT user_id, ((wins*1.0) / games) AS winrate FROM playerstats WHERE games >= ? ORDER BY winrate DESC", (min_games,))
                i = 0
                for (user_id, winrate) in c.fetchall():
                    user = globvars.client.get_user(user_id)
                    if not user:
                        continue
                    i += 1
                    msg += f"{i}. **{utils.escape_markdown(user.name)}** - {winrate * 100:.1f}%\n"
                    if i >= limit:
                        break
            else:
                msg = language["cmd"]["top_usage"]

        await ctx.send(msg)
