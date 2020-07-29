"""Playtest command cog"""

import botutils
import json
import configparser
from ._admin import Admin
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

PLAYTESTERS = json.loads(Config["misc"]["PLAYTESTERS"])


class Playtest(Admin):
    """Playtest command"""

    # ---------- PLAYTEST COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "playtest")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def playtest(self, ctx):
        """Playtest command"""
        
        import globvars
        playtesters = PLAYTESTERS
        for userid in playtesters:
            globvars.master_state.pregame.safe_add_player(userid)
        globvars.master_state.game = globvars.master_state.game_packs["botc"]["game_obj"]
        await globvars.master_state.game.start_game()
