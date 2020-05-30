"""Contains event listeners"""

from discord.ext import commands

class Listeners(commands.Cog):
    """Event listeners"""
    
    def __init__(self, client):
        self.client = client
      
    @commands.Cog.listener()
    async def on_ready(self):
        """On_ready event"""
        print(f"Logged in as {self.client.user.name}")
        print(f"Bot ID {self.client.user.id}")
        print("----------")

def setup(client):
    client.add_cog(Listeners(client))
