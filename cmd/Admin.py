"""Contains admins only commands"""

import configparser
import traceback
import json
import globvars
import discord
import botutils
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

fjoin_str = language["cmd"]["fjoin"]
fjoined_str = language["cmd"]["fjoined"]
fleave_str = language["cmd"]["fleave"]
fleaved_str = language["cmd"]["fleaved"]
user_not_found_str = language["errors"]["user_not_found"]
missing_user_str = language["errors"]["missing_user"]
error_str = language["system"]["error"]


class Admin(commands.Cog, name="Admin Commands"):
    """Admins only commands cog"""
    
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return botutils.check_if_admin(ctx)
    

    # ---------- FJOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "fjoin")
    async def fjoin(self, ctx, *, member: discord.Member):
        """Force join command"""

        import main
        if globvars.master_state.pregame.is_joined(member.id):
            await ctx.send(fjoined_str.format(ctx.author.mention, member.name))
        else:
            globvars.master_state.pregame.safe_add_player(member.id)
            await ctx.send(fjoin_str.format(member.name, len(globvars.master_state.pregame)))
        await botutils.add_alive_role(member)
    

    # ---------- FLEAVE COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "fleave")
    async def fleave(self, ctx, *, member: discord.Member):
        """Force leave command"""

        import main
        if globvars.master_state.pregame.is_joined(member.id):
            globvars.master_state.pregame.safe_remove_player(member.id)
            await ctx.send(fleave_str.format(member.name, len(globvars.master_state.pregame)))
        else:
            await ctx.send(fleaved_str.format(ctx.author.mention, member.name))
        await botutils.remove_alive_role(member)


    async def cog_command_error(self, ctx, error):
        """Error handling on command"""

        # Case: bad argument (user not found)
        if isinstance(error, commands.BadArgument):
            await ctx.send(user_not_found_str.format(ctx.author.mention))
            return
        # Case: missing required argument (user not specified)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(missing_user_str.format(ctx.author.mention))
            return
        elif isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
      

def setup(client):
    client.add_cog(Admin(client))
