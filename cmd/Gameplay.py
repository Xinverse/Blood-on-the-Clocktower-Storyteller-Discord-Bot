"""Contains the Gamplay cog: gameplay related commands"""

import botutils
import traceback
import json
import configparser
import globvars
import botc
from datetime import datetime, timezone
from botutils import after_lobby_timeout, lobby_timeout
from discord.ext import commands, tasks

Config = configparser.ConfigParser()

Config.read("config.INI")
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
ALIVE_ROLE_ID = int(ALIVE_ROLE_ID)

Config.read("preferences.INI")
LOBBY_TIMEOUT = Config["duration"]["LOBBY_TIMEOUT"]
LOBBY_TIMEOUT = int(LOBBY_TIMEOUT)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

join_str = language["cmd"]["join"]
joined_str = language["cmd"]["joined"]
quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]
error_str = language["system"]["error"]
cooldown_str = language["errors"]["cmd_cooldown"]
lobby_timeout_str = language["system"]["lobby_timeout"]
time_pregame = language["cmd"]["time_pregame"]


class Gamplay(commands.Cog, name="Gameplay Commands"):
    """Gamplay cog"""
    
    def __init__(self, client):

        self.client = client

    
    def cog_check(self, ctx):
        """Global check for all commands of this cog: ignored users may not use commands"""
        
        return botutils.check_if_not_ignored(ctx)
    

    # ---------- PLAYTEST COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "playtest")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def playtest(self, ctx):
        """Playtest command"""
        playtesters = [
            600426113285750785,
            606332710989856778,
            635674760247771136,
            614109280508968980,
            270904126974590976
            #159985870458322944,
            #184405311681986560,
            #235088799074484224,
            #460105234748801024,
            #438057969251254293
            ]
        for userid in playtesters:
            globvars.master_state.pregame.safe_add_player(userid)
        globvars.master_state.game = globvars.master_state.game_packs["botc"]["game_obj"]
        await globvars.master_state.game.start_game()


def setup(client):
    client.add_cog(Gamplay(client))
