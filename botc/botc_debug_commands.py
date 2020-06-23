"""Contains the botc debug/admin cog"""

from discord.ext import commands


class BoTCDebugCommands(commands.Cog, name = "BoTC debug commands"):
    """BoTC in-game debug commands cog"""

    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        pass