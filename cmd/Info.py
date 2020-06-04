"""Contains the Info cog: general bot, gameplay information, credits"""

import discord
import configparser
import traceback
import json 
import botutils
import globvars
from discord.ext import commands
from time import time
from datetime import timedelta

Config = configparser.ConfigParser()

Config.read("preferences.INI")
COLOR = Config["colors"]["CARD_NORMAL"]
COLOR = int(COLOR, 16)

Config.read("config.INI")
PREFIX = Config["settings"]["PREFIX"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

github_str = language["cmd"]["github"]
uptime_str = language["cmd"]["uptime"]
ping_str = language["cmd"]["ping"]
error_str = language["system"]["error"]

class Info(commands.Cog, name="Information Commands"):
    """Info cog"""
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_not_ignored(ctx)


    # ---------- GITHUB COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "github", aliases = ["git"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def github(self, ctx):
        await ctx.send(github_str)
    

    # ---------- PING COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "ping", aliases = ["pong"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def ping(self, ctx):
        """Check the latency."""

        await ctx.send(ping_str.format(round(self.client.latency, 4)))


    # ---------- UPTIME COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "uptime")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def uptime(self, ctx):
        """Check the uptime."""

        uptime = time() - globvars.master_state.boottime
        uptime = round(uptime)
        uptime_formatted = str(timedelta(seconds=uptime))
        await ctx.send(uptime_str.format(uptime_formatted))
    

    async def cog_command_error(self, ctx, error):
        """Error handling on commands"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Info(client))