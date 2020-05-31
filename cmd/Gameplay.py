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
DAY_PHASE = Config["duration"]["DAY_PHASE"]
DAY_PHASE = int(DAY_PHASE)
NIGHT_PHASE = Config["duration"]["NIGHT_PHASE"]
NIGHT_PHASE = int(NIGHT_PHASE)

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

join_str = language["cmd"]["join"]
joined_str = language["cmd"]["joined"]
quit_str = language["cmd"]["quit"]
quitted_str = language["cmd"]["quitted"]
error_str = language["system"]["error"]
cooldown_str = language["errors"]["cmd_cooldown"]
lobby_timeout_str = language["system"]["lobby_timeout"]

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
    main.master_state.pregame.clear()

# ---------- NIGHT PHASE LOOP ----------------------------------------

@tasks.loop(seconds=NIGHT_PHASE, count=2)
async def night_phase():
    """Lobby timeout loop"""
    pass

# ---------- DAY PHASE LOOP ----------------------------------------

@tasks.loop(seconds=DAY_PHASE, count=2)
async def day_phase():
    """Lobby timeout loop"""
    pass


class Gamplay(commands.Cog, name="Gameplay Commands"):
    """Gamplay cog"""
    
    def __init__(self, client):
        self.client = client
        global local_client
        local_client = self.client
    
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
            # If you are the first player to join the game, then start the lobby timeout loop
            if len(main.master_state.pregame) == 1:
                lobby_timeout.start()
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
        else:
            await ctx.send(quitted_str.format(ctx.author.mention))
        await botutils.remove_alive_role(self.client, ctx.author)
    

     # ---------- TIME COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "time", aliases = ["t"])
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def time(self, ctx):
        """Time command"""
        import main
        # If the pre-game lobby contains people, send the time remaining message
        if len(main.master_state.pregame):
            now = datetime.now(timezone.utc)
            finish = lobby_timeout.next_iteration
            time_left = finish - now
            await ctx.send(str(time_left.total_seconds()))
        else:
            pass


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
