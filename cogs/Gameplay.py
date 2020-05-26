"""Contains the Gamplay cog: gameplay related commands"""

import discord
from discord.ext import commands

class Gamplay(commands.Cog):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Gamplay(client))
