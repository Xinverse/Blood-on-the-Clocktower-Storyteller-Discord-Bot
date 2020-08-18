"""Contains the on_command_error event listener"""

#import sys
import botutils
import json
import traceback
from discord.ext import commands

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

error_str = language["system"]["error"]


class on_command_error(commands.Cog):
    """Event listener on_command_error"""
    
    def __init__(self, client):
        self.client = client
    
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
            #print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            # Log the error
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc())


def setup(client):
    client.add_cog(on_command_error(client))
