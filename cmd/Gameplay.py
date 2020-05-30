"""Contains the Gamplay cog: gameplay related commands"""

import botutils
import json
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

join_str = language["cmd"]["join"]
joined_str = language["cmd"]["joined"]
quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]


class Gamplay(commands.Cog):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
    

    # ---------- JOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "join", aliases = ["j"])
    @commands.check(botutils.check_if_lobby)
    @commands.check(botutils.check_if_not_ignored)
    async def join(self, ctx):
        """Join command"""
        import main
        if main.master_state.pregame.is_joined(ctx.author.id):
            await ctx.send(joined_str.format(ctx.author.mention))
        else:
            main.master_state.pregame.safe_add_player(ctx.author.id)
            await ctx.send(join_str.format(ctx.author.name, len(main.master_state.pregame)))
        await botutils.add_alive_role(self.client, ctx.author)

    
    # ---------- QUIT COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "quit", aliases = ["q"])
    @commands.check(botutils.check_if_lobby)
    @commands.check(botutils.check_if_not_ignored)
    async def quit(self, ctx):
        """Join command"""
        import main
        if main.master_state.pregame.is_joined(ctx.author.id):
            main.master_state.pregame.safe_remove_player(ctx.author.id)
            await ctx.send(quit_str.format(ctx.author.name, len(main.master_state.pregame)))
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        await botutils.remove_alive_role(self.client, ctx.author)
        

def setup(client):
    client.add_cog(Gamplay(client))
