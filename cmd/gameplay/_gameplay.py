"""Contains the gameplay cog"""

import botutils
import json
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)


class Gameplay(commands.Cog, name = language["system"]["gameplay_cog"]):
    """Gamplay cog"""
    
    def __init__(self, client):

        self.client = client

    
    def cog_check(self, ctx):
        """Global check for all commands of this cog: ignored users may not use commands"""
        
        return botutils.check_if_not_ignored(ctx)
