"""Contains the Gamplay cog: gameplay related commands"""

import discord
import botutils
from discord.ext import commands

class Gamplay(commands.Cog):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, aliases = ["seatings", "seat", "seats"])
    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def seating(self, ctx):
        """Stats command"""
        await ctx.send("To-do")

def setup(client):
    client.add_cog(Gamplay(client))
