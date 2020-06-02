"""Contains the Gamplay cog: gameplay related commands"""

import botutils
import traceback
import json
import configparser
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

# the client object, stored locally
local_client = None

# ---------- LOBBY TIMEOUT LOOP ----------------------------------------

@tasks.loop(seconds=LOBBY_TIMEOUT, count=2)
async def lobby_timeout():
    """Lobby timeout loop"""
    pass

@lobby_timeout.after_loop
async def after_lobby_timeout():
    """After lobby timeout"""
    global local_client
    import main
    # Only send the lobby timeout message if someone is still in the game
    if not lobby_timeout.is_being_cancelled():
        await botutils.send_lobby(local_client, lobby_timeout_str.format(botutils.make_role_ping(ALIVE_ROLE_ID)))
    # Remove the alive role from everyone
    await botutils.remove_all_alive_roles_pregame(local_client)
    # Clear the master pregame state
    main.master_state.transition_to_empty()


class Gamplay(commands.Cog, name="Gameplay Commands"):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
        global local_client
        local_client = self.client
    
    def cog_check(self, ctx):
        """Global check for all commands of this cog: ignored users may not use commands"""
        return botutils.check_if_not_ignored(ctx)

    
    # ---------- ROLE COMMAND ----------------------------------------
    @commands.group(pass_context=True, name = "role")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def role(self, ctx):
        """Role command"""

        if ctx.invoked_subcommand is None:
            await ctx.send("Role command")
    
    @role.command()
    async def all(self, ctx, *, role_name):
        import main
        test = str(main.master_state.game_packs)
        await ctx.send(test)
    

    # ---------- JOIN COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "join", aliases = ["j"])
    @commands.check(botutils.check_if_lobby)
    @commands.check(botutils.check_if_not_in_game)
    async def join(self, ctx):
        """Join command"""

        import main

        # The command user has already joined
        if main.master_state.pregame.is_joined(ctx.author.id):
            await ctx.send(joined_str.format(ctx.author.mention))

        # The command user has not joined yet; make them join
        else:
            main.master_state.pregame.safe_add_player(ctx.author.id)
            await ctx.send(join_str.format(ctx.author.name, len(main.master_state.pregame)))
            # If you are the first player to join the game, then start the lobby timeout loop
            if main.master_state.session == botutils.BotState.empty:
                lobby_timeout.start()
                main.master_state.transition_to_pregame()

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
            # If you are the last player to leave, then cancel the lobby timeout loop
            if len(main.master_state.pregame) == 0:
                lobby_timeout.cancel()
                main.master_state.transition_to_empty()
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        await botutils.remove_alive_role(self.client, ctx.author)
    

    # ---------- STATS COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "stats", aliases = ["statistics"])
    @commands.check(botutils.check_if_lobby_or_spec_or_dm_or_admin)
    @commands.check(botutils.check_if_not_in_empty)
    async def stats(self, ctx):
        """Stats command"""

        import main
        # If we are in pregame:
        if main.master_state.session == botutils.BotState.pregame:
            await botutils.send_pregame_stats(self.client, ctx, main.master_state.pregame.list)
        # If we are in game:
        elif main.master_state.session == botutils.BotState.game:
            pass
    

    # ---------- TIME COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "time", aliases = ["t"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    @commands.check(botutils.check_if_not_in_empty)
    async def time(self, ctx):
        """Time command"""

        import main
        # If we are in pregame:
        if main.master_state.session == botutils.BotState.pregame:
            now = datetime.now(timezone.utc)
            finish = lobby_timeout.next_iteration
            time_left = finish - now
            time_left = time_left.total_seconds()
            time_left = round(time_left)
            msg = time_pregame.format(botutils.make_time_string(time_left), botutils.make_time_string(LOBBY_TIMEOUT))
            await ctx.send(msg)
        # If we are in game:
        elif main.master_state.session == botutils.BotState.game:
            pass


    async def cog_command_error(self, ctx, error):
        """Error handling on commands"""

        # Case: check failure
        if isinstance(error, commands.errors.CheckFailure):
            return

        # Case: command on cooldown
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(cooldown_str.format(ctx.author.mention))

        # For other cases we will want to see the error
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(self.client, botutils.Level.error, traceback.format_exc()) 
    

    async def cog_after_invoke(self, ctx):
        """After invoking each command of this cog, perform some state checks"""

        import main
        main.master_state.sync_state()


def setup(client):
    client.add_cog(Gamplay(client))
