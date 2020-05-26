"""Contains the Fun cog: fun related commands"""

import discord
import botutils
import random
from discord.ext import commands
from time import time
from datetime import timedelta

class Fun(commands.Cog):
    """Fun cog"""
    
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def dog(self, ctx):
        """Dog command"""
        await ctx.send("Did the dog land on its feet?")

    @commands.command(pass_context=True, aliases = ["pong"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def ping(self, ctx):
        """Ping command"""
        await ctx.send(':ping_pong: **Pong!** Latency: **{0}** seconds.'.format(round(self.client.latency, 4)))

    @commands.command(pass_context=True)
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def uptime(self, ctx):
        """Uptime command"""
        from main import bootTime
        uptime = time() - bootTime
        uptime = round(uptime)
        uptime_str = str(timedelta(seconds=uptime))
        await ctx.send(f":clock: **uptime:** {uptime_str}")
    
    @commands.command(pass_context=True, aliases = ["flip"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def coin(self, ctx):
        """Coin command"""
        possibilities = ['heads'] * 50 + ['tails'] * 50 + ['side'] * 1
        result = random.choice(possibilities)
        await ctx.send(f"The coin landed on its **{result}**")


def setup(client):
    client.add_cog(Fun(client))
