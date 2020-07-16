"""Contains the on_command event listener"""

import discord
import json
import configparser
import botutils
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("preferences.INI")

IGNORE_THRESHOLD = int(Config["duration"]["IGNORE_THRESHOLD"])
TOKENS_GIVEN = int(Config["duration"]["TOKENS_GIVEN"])
TOKEN_RESET = int(Config["duration"]["TOKEN_RESET"])

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

ignore = language["system"]["ignore"]


class on_command(commands.Cog):
    """Event listener on_ready"""
    
    def __init__(self, client):
        self.client = client
      
    @commands.Cog.listener()
    async def on_command(self, ctx):
        """on_command event"""

        import globvars
        
        # For each command used, we increase the count by one
        if str(ctx.author.id) not in globvars.ratelimit_dict:
            globvars.ratelimit_dict[str(ctx.author.id)] = 1
        else:
            globvars.ratelimit_dict[str(ctx.author.id)] += 1
        
        # The user has surpassed the threshold, and will be ignored
        if globvars.ratelimit_dict[str(ctx.author.id)] > IGNORE_THRESHOLD:
            if not ctx.author.id in globvars.ignore_list:
                globvars.ignore_list.append(ctx.author.id)
                msg = f"{ctx.author.mention} was added to the ignore list for rate limiting."
                await botutils.log(botutils.Level.warning, msg)
                await ctx.send(ignore.format(ctx.author.mention, IGNORE_THRESHOLD, TOKEN_RESET))

        if globvars.ratelimit_dict[str(ctx.author.id)] >= TOKENS_GIVEN:
            pass


def setup(client):
    client.add_cog(on_command(client))
