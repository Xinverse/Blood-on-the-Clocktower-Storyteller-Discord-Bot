"""Contains the Gamplay cog: gameplay related commands"""

import botutils
import traceback
import json
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

join_str = language["cmd"]["join"]
joined_str = language["cmd"]["joined"]
quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]
error_str = language["system"]["error"]
cooldown_str = language["errors"]["cmd_cooldown"]

class Gamplay(commands.Cog, name="Gameplay Commands"):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        return botutils.check_if_not_ignored(ctx)
    

    # ---------- JOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "join", aliases = ["j"])
    @commands.check(botutils.check_if_lobby)
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
    async def quit(self, ctx):
        """Join command"""

        import main
        if main.master_state.pregame.is_joined(ctx.author.id):
            main.master_state.pregame.safe_remove_player(ctx.author.id)
            await ctx.send(quit_str.format(ctx.author.name, len(main.master_state.pregame)))
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        await botutils.remove_alive_role(self.client, ctx.author)
    

    # ---------- STATS COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "stats", aliases = ["statistics"])
    @commands.check(botutils.check_if_lobby)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def stats(self, ctx):
        """Stats command"""

        import main
        msg = "Statistics"
        await ctx.send(msg)
    

    async def cog_command_error(self, ctx, error):
        """Error handling on commands"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(cooldown_str.format(ctx.author.mention))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(self.client, botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Gamplay(client))
