"""Contains the Info cog: general bot, gameplay information, credits"""

import discord
import configparser
import json 
import botutils
from discord.ext import commands

Config = configparser.ConfigParser()

Config.read("preferences.INI")
COLOR = Config["colors"]["CARD_NORMAL"]
COLOR = int(COLOR, 16)

Config.read("config.INI")
PREFIX = Config["settings"]["PREFIX"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

github_str = language["cmd"]["github"]

class Info(commands.Cog):
    """Info cog"""
    
    def __init__(self, client):
        self.client = client


    # ---------- GITHUB COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "github", aliases = ["git"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    @commands.check(botutils.check_if_not_ignored)
    async def github(self, ctx):
        await ctx.send(github_str)


def setup(client):
    client.add_cog(Info(client))