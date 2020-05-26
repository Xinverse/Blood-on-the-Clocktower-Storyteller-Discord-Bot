"""Contains the Fun cog: fun related commands"""

import discord
import botutils
from discord.ext import commands

class Fun(commands.Cog):
    """Fun cog"""
    
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.check(botutils.check_if_lobby_or_dm)
    async def dog(self, ctx):
        await ctx.send("Did the dog land on its feet?")

    @commands.command(pass_context=True, aliases = ["pong"])
    @commands.check(botutils.check_if_lobby_or_dm)
    async def ping(self, ctx):
        await ctx.send(':ping_pong: **Pong!** Latency: **{0}** seconds.'.format(round(self.client.latency, 4)))

def setup(client):
    client.add_cog(Fun(client))
