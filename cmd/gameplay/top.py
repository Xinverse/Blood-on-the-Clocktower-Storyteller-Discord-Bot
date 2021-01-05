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
        limit = Config["misc"]["TOP_LIMIT"]

        with sqlite3.connect("data.sqlite3") as db:
            if arg == "games":
                c = db.execute("SELECT user_id, games FROM playerstats ORDER BY games DESC LIMIT ?", (limit,))
                msg = f"__Top {limit} by games played__\n\n"
                for (i, (user_id, games)) in enumerate(c.fetchall()):
                    user = globvars.client.get_user(user_id)
                    if user:
                        name = user.display_name
                    else:
                        name = str(user_id)
                    msg += f"{i + 1}. **{utils.escape_markdown(name)}** - {games}\n"
            elif arg == "wins":
                msg = f"__Top {limit} by games won__\n\n"
                c = db.execute("SELECT user_id, wins FROM playerstats ORDER BY wins DESC LIMIT ?", (limit,))
                for (i, (user_id, wins)) in enumerate(c.fetchall()):
                    user = globvars.client.get_user(user_id)
                    if user:
                        name = user.display_name
                    else:
                        name = str(user_id)
                    msg += f"{i + 1}. **{utils.escape_markdown(name)}** - {wins}\n"
            elif arg == "winrate":
                msg = f"__Top {limit} by win rate__\n\n"
                c = db.execute("SELECT user_id, ((wins*1.0) / games) AS winrate FROM playerstats WHERE games >= 15 ORDER BY winrate DESC LIMIT ?", (limit,))
                for (i, (user_id, winrate)) in enumerate(c.fetchall()):
                    user = globvars.client.get_user(user_id)
                    if user:
                        name = user.display_name
                    else:
                        name = str(user_id)
                    msg += f"{i + 1}. **{utils.escape_markdown(name)}** - {winrate * 100:.1f}%\n"
            else:
                msg = "Argument must be one of `games`, `wins` or `winrate`."

        await ctx.send(msg)
