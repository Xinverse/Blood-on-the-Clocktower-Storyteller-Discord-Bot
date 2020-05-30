"""Contains the Gamplay cog: gameplay related commands"""

import botutils
from discord.ext import commands

class Gamplay(commands.Cog):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, name = "join", aliases = ["j"])
    @commands.check(botutils.check_if_lobby)
    async def join(self, ctx):
        """Join command"""
        await botutils.add_alive_role(self.client, ctx.author)
        await ctx.send(f"{ctx.author.name} joined the game.")

def setup(client):
    client.add_cog(Gamplay(client))
