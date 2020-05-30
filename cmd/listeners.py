"""Contains event listeners"""

import sys
import json
import botutils
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

restart_msg = language["system"]["restart"]


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
        await botutils.log(self.client, botutils.Level.info, restart_msg)


def setup(client):
    client.add_cog(Listeners(client))
