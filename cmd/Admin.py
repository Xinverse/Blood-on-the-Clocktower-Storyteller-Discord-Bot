"""Contains admins only commands"""

import configparser
import json
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


class Admin(commands.Cog):
    """Admins only commands cog"""
    
    def __init__(self, client):
        self.client = client
    

    # ---------- FJOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "fjoin")
    @commands.check(botutils.check_if_admin)
    async def fjoin(self, ctx, *, member: discord.Member):
        """Force join command"""

        import main
        if main.master_state.pregame.is_joined(member.id):
            await ctx.send(fjoined_str.format(ctx.author.mention, member.name))
        else:
            main.master_state.pregame.safe_add_player(member.id)
            await ctx.send(fjoin_str.format(member.name, len(main.master_state.pregame)))
        await botutils.add_alive_role(self.client, member)
    
    @fjoin.error
    async def fjoin_error(self, ctx, error):
        """Error handling on fjoin command"""

        if isinstance(error, commands.BadArgument):
            await ctx.send(user_not_found_str.format(ctx.author.mention))


    # ---------- FLEAVE COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "fleave")
    @commands.check(botutils.check_if_admin)
    async def fleave(self, ctx, *, member: discord.Member):
        """Force leave command"""

        import main
        if main.master_state.pregame.is_joined(member.id):
            main.master_state.pregame.safe_remove_player(member.id)
            await ctx.send(fleave_str.format(member.name, len(main.master_state.pregame)))
        else:
            await ctx.send(fleaved_str.format(ctx.author.mention, member.name))
        await botutils.remove_alive_role(self.client, member)

    @fleave.error
    async def fleave_error(self, ctx, error):
        """Error handling on fleave command"""

        # Case: bad argument (user not found)
        if isinstance(error, commands.BadArgument):
            await ctx.send(user_not_found_str.format(ctx.author.mention))
      

def setup(client):
    client.add_cog(Admin(client))
