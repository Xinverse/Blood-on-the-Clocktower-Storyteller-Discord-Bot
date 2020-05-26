"""Contains the Info cog: general bot, gameplay information, credits"""

import discord
import configparser
import json 
import botutils
from discord.ext import commands
from discord.ext import commands

Config = configparser.ConfigParser()

Config.read("preferences.INI")
color = Config["colors"]["CARD_NORMAL"]
color = int(color, 16)

Config.read("config.INI")
PREFIX = Config["settings"]["PREFIX"]

with open('lorestore.json') as json_file: 
    lorestore = json.load(json_file) 

copyrights_str = lorestore["misc"]["copyrights"]
how_to_play = lorestore["info"]["how_to_play"]

class Info(commands.Cog):
    """Info cog"""
    
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases = ["git"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def github(self, ctx):
        await ctx.send("The Github page of the bot can be found here: " \
                       "<https://github.com/Xinverse/BOTC-Bot>")

    @commands.command(pass_context=True, aliases = ["credit", "cred"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def credits(self, ctx):
        embed = discord.Embed(title="CREDITS - Blood on the Clocktower [Storyteller Bot]", color=color)
        embed.set_author(name="Discord Werewolf Server", icon_url=self.client.get_guild(ctx.guild.id).icon_url)
        embed.set_footer(text=copyrights_str)
        msg1 = "Programming by **Xinverse#4011**. Please privately message them for any bugs or suggestions."
        embed.add_field(name="**Developer**", value=msg1, inline=False)
        msg2 = "Special thanks to the team of administrators of Discord Werewolf for their valuable " \
               "input, suggestions and support. The copyrights of Blood on the Clocktower (BoTC) are " \
               "owned by The Pandemonium Institute (TPI). This Discord adaptation of BoTC is an " \
               "independent project, and the Developer is not affiliated with TPI in any way."
        embed.add_field(name="**Acknowledgements**", value=msg2, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases = ["information"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def info(self, ctx):
        embed = discord.Embed(title="INFO - Blood on the Clocktower [Storyteller Bot]", color=color)
        embed.set_author(name="Discord Werewolf Server", icon_url=self.client.get_guild(ctx.guild.id).icon_url)
        embed.set_footer(text=copyrights_str)
        msg1 = how_to_play
        embed.add_field(name="**What is Blood on the Clocktower?**", value=msg1, inline=False)
        msg2 = f"To join a game, use `{PREFIX}join`. For a list of roles, use `{PREFIX}roles`."
        embed.add_field(name="**Getting started**", value=msg2, inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))