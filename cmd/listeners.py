"""Contains event listeners"""

import json
import sys
import traceback
import discord
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
        activity = discord.Activity(name='BOTC', type=discord.ActivityType.playing)
        await self.client.change_presence(activity=activity)
        await botutils.log(botutils.Level.info, restart_msg)
    
    @commands.Cog.listener()
    async def on_error(self, event):
        """On_error event"""
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        try:
            raise event
        except Exception as e:
            await botutils.log(botutils.Level.error, e)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        
        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(Listeners(client))
