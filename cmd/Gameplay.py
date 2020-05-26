"""Contains the Gamplay cog: gameplay related commands"""

import discord
import botutils
from discord.ext import commands

class Gamplay(commands.Cog):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
    
    async def add_alive_role(self, member_obj):
        """Grand the alive role to a player"""
        role = self.client.get_guild(int(607281213341958177)).get_role(int(714608751872704542))
        await member_obj.add_roles(role)

    @commands.command(pass_context=True, aliases = ["j"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def join(self, ctx):
        """Seating command"""
        await self.add_alive_role(ctx.author)
        await ctx.send(f"{ctx.author.name} joined the game.")
    
    @commands.command(pass_context=True, aliases = ["seatings", "seat", "seats"])
    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def seating(self, ctx):
        """Seating command"""
        await ctx.send("To-do")

def setup(client):
    client.add_cog(Gamplay(client))
