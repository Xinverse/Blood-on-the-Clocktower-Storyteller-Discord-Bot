"""Contains the Fun cog: fun related commands"""

import botutils
import random
import json
from discord.ext import commands
from time import time
from datetime import timedelta

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

dog_str = language["cmd"]["dog"]
ping_str = language["cmd"]["ping"]
uptime_str = language["cmd"]["uptime"]

class Fun(commands.Cog):
    """Fun cog"""
    
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name = "dog")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def dog(self, ctx):
        """Flip a dog."""
        await ctx.send(dog_str)

    @commands.command(pass_context=True, name = "ping", aliases = ["pong"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def ping(self, ctx):
        """Check the latency."""
        await ctx.send(ping_str.format(round(self.client.latency, 4)))

    @commands.command(pass_context=True, name = "uptime")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def uptime(self, ctx):
        """Check the uptime."""
        from main import bootTime
        uptime = time() - bootTime
        uptime = round(uptime)
        uptime_formatted = str(timedelta(seconds=uptime))
        await ctx.send(uptime_str.format(uptime_formatted))

def setup(client):
    client.add_cog(Fun(client))
