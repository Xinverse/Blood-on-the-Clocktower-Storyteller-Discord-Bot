"""Contains admins only commands"""

import discord
import botutils
from discord.ext import commands

class Admin(commands.Cog):
    """Admins only commands cog"""
    
    def __init__(self, client):
        self.client = client
      
      
def setup(client):
    client.add_cog(Admin(client))
