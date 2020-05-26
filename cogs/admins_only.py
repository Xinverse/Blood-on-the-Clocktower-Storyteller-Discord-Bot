"""Contains admins only commands"""

import discord
from discord.ext import commands

class AdminsOnly(commands.Cog):
    """Admins only commands cog"""
    
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(AdminsOnly(client))