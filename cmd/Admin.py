"""Contains admins only commands"""

import discord
import botutils
from discord.ext import commands

class Admin(commands.Cog):
    """Admins only commands cog"""
    
    def __init__(self, client):
        self.client = client
      
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.client.user.name}")
        print(f"Bot ID {self.client.user.id}")
        print("----------")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await ctx.send("Command detected")

def setup(client):
    client.add_cog(Admin(client))
