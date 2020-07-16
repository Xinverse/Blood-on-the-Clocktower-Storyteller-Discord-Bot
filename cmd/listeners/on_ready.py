"""Contains the on_ready event listener"""

import json
import botutils
import discord
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

restart_msg = language["system"]["restart"]


class on_ready(commands.Cog):
    """Event listener on_ready"""
    
    def __init__(self, client):
        self.client = client
      
    @commands.Cog.listener()
    async def on_ready(self):
        """On_ready event"""
        
        print(f"Logged in as {self.client.user.name}")
        print(f"Bot ID {self.client.user.id}")
        print("----------")
        activity = discord.Activity(name='Blood on the Clocktower', type=discord.ActivityType.playing)
        await self.client.change_presence(activity=activity)
        await botutils.log(botutils.Level.info, restart_msg)

def setup(client):
    client.add_cog(on_ready(client))
