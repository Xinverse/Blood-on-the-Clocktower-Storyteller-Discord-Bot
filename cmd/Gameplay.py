"""Contains the Gamplay cog: gameplay related commands"""

import botutils
import traceback
import json
import configparser
import globvars
import botc
from datetime import datetime, timezone
from discord.ext import commands, tasks

Config = configparser.ConfigParser()

Config.read("config.INI")
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
ALIVE_ROLE_ID = int(ALIVE_ROLE_ID)

Config.read("preferences.INI")
LOBBY_TIMEOUT = Config["duration"]["LOBBY_TIMEOUT"]
LOBBY_TIMEOUT = int(LOBBY_TIMEOUT)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

join_str = language["cmd"]["join"]
joined_str = language["cmd"]["joined"]
quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]
error_str = language["system"]["error"]
cooldown_str = language["errors"]["cmd_cooldown"]
lobby_timeout_str = language["system"]["lobby_timeout"]
time_pregame = language["cmd"]["time_pregame"]


# ---------- LOBBY TIMEOUT LOOP ----------------------------------------

@tasks.loop(seconds=LOBBY_TIMEOUT, count=2)
async def lobby_timeout():
    """Lobby timeout loop"""
    pass

@lobby_timeout.after_loop
async def after_lobby_timeout():
    """After lobby timeout"""
    # Only send the lobby timeout message if someone is still in the game
    
    if not lobby_timeout.is_being_cancelled():
        await botutils.send_lobby(lobby_timeout_str.format(botutils.make_role_ping(ALIVE_ROLE_ID)))
    # Remove the alive role from everyone
    await botutils.remove_all_alive_roles_pregame()
    # Clear the master pregame state
    globvars.master_state.pregame.clear()
    botutils.update_state_machine()


class Gamplay(commands.Cog, name="Gameplay Commands"):
    """Gamplay cog"""
    
    def __init__(self, client):

        self.client = client

    
    def cog_check(self, ctx):
        """Global check for all commands of this cog: ignored users may not use commands"""
        
        return botutils.check_if_not_ignored(ctx)

    
    # ---------- START COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "fstart")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def fstart(self, ctx):
        """Force start command"""
        globvars.master_state.game = globvars.master_state.game_packs["botc"]["game_obj"]
        await globvars.master_state.game.start_game()
        globvars.client.load_extension("botc.botc_commands")
    

    # ---------- PLAYTEST COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "playtest")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def playtest(self, ctx):
        """Playtest command"""
        playtesters = [
            600426113285750785,
            606332710989856778,
            635674760247771136,
            614109280508968980,
            270904126974590976,
            159985870458322944,
            184405311681986560,
            235088799074484224,
            460105234748801024,
            438057969251254293
            ]
        for userid in playtesters:
            globvars.master_state.pregame.safe_add_player(userid)
        globvars.master_state.game = globvars.master_state.game_packs["botc"]["game_obj"]
        await globvars.master_state.game.start_game()

    
    # ---------- ROLE COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "role", aliases = ["roles"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def role(self, ctx, *, role_name):
        """Role command"""

        found = botutils.find_role_in_all(role_name)
        
        # We did not find the role, send them the whole list
        if found is None:
            await ctx.send(globvars.master_state.game_packs["botc"]["formatter"].create_complete_roles_list())

        # We found the role, send them that role card only
        else:
            await found.send_role_card_embed(ctx)

    @role.error
    async def role_error(self, ctx, error):
        """Error handling of the role command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # Case: missing argument -> we will print the entire list of roles
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(globvars.master_state.game_packs["botc"]["formatter"].create_complete_roles_list())
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- JOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "join", aliases = ["j"])
    @commands.check(botutils.check_if_lobby)
    @commands.check(botutils.check_if_not_in_game)
    async def join(self, ctx):
        """Join command"""

        # The command user has already joined
        if globvars.master_state.pregame.is_joined(ctx.author.id):
            await ctx.send(joined_str.format(ctx.author.mention))

        # The command user has not joined yet; make them join
        else:
            globvars.master_state.pregame.safe_add_player(ctx.author.id)
            botutils.update_state_machine()
            await ctx.send(join_str.format(ctx.author.name, len(globvars.master_state.pregame)))
            # If you are the first player to join the game, then start the lobby timeout loop
            if len(globvars.master_state.pregame) == 1:
                lobby_timeout.start()

        # Still give everyone the role just in case of discord sync issue
        await botutils.add_alive_role(ctx.author)
    
    @join.error
    async def join_error(self, ctx, error):
        """Error handling of the join command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
        
    
    # ---------- QUIT COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "quit", aliases = ["q", "leave"])
    @commands.check(botutils.check_if_lobby)
    async def quit(self, ctx):
        """Quit command"""
        
        # The command user has joined; make them quit
        if globvars.master_state.pregame.is_joined(ctx.author.id):
            globvars.master_state.pregame.safe_remove_player(ctx.author.id)
            botutils.update_state_machine()
            await ctx.send(quit_str.format(ctx.author.name, len(globvars.master_state.pregame)))
            # If you are the last player to leave, then cancel the lobby timeout loop
            if len(globvars.master_state.pregame) == 0:
                lobby_timeout.cancel()
        
        # The command user has not joined
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        
        # Still take away the role from everyone just in case of discord sync issue
        await botutils.remove_alive_role(ctx.author)
    
    @quit.error
    async def quit_error(self, ctx, error):
        """Error handling of the quit command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
    

    # ---------- STATS COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "stats", aliases = ["statistics"])
    @commands.check(botutils.check_if_lobby_or_spec_or_dm_or_admin)
    @commands.check(botutils.check_if_not_in_empty)
    async def stats(self, ctx):
        """Stats command"""

        # If we are in pregame:
        if globvars.master_state.session == botutils.BotState.pregame:
            await botutils.send_pregame_stats(ctx, globvars.master_state.pregame.list)

        # If we are in game:
        elif globvars.master_state.session == botutils.BotState.game:
            pass
    
    @stats.error
    async def stats_error(self, ctx, error):
        """Error handling of the stats command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
    

    # ---------- TIME COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "time", aliases = ["t"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    @commands.check(botutils.check_if_not_in_empty)
    async def time(self, ctx):
        """Time command"""

        # If we are in pregame:
        if globvars.master_state.session == botutils.BotState.pregame:
            now = datetime.now(timezone.utc)
            finish = lobby_timeout.next_iteration
            time_left = finish - now
            time_left = time_left.total_seconds()
            time_left = round(time_left)
            msg = time_pregame.format(botutils.make_time_string(time_left), botutils.make_time_string(LOBBY_TIMEOUT))
            await ctx.send(msg)

        # If we are in game:
        elif globvars.master_state.session == botutils.BotState.game:
            pass
    
    @time.error
    async def time_error(self, ctx, error):
        """Error handling of the time command"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return
        
        # For other cases we will want to see the error logged
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


def setup(client):
    client.add_cog(Gamplay(client))
