"""Contains the cog for BoTC in-game commands"""

import configparser
import botutils
import traceback
import json
import globvars
from discord.ext import commands
from botc import BOTCUtils, NotAPlayer, PlayerParser, RoleCannotUseCommand
from botc.gamemodes.troublebrewing._utils import TBRole

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]


def check_if_is_player(ctx):
    """Return true if user is a player, and not in fleaved state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player:
        if player.is_fleaved():
            raise NotAPlayer("Command not allowed: user has quit the game (BoTC).")
        else:
            return True
    else:
        raise NotAPlayer("Command not allowed: user is not a player (BoTC).")


def check_if_can_serve(ctx):
    """Can serve: butler"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.butler.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use serve command (BoTC)")


def check_if_can_poison(ctx):
    """Can poison: poisoner"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.poisoner.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use poison command (BoTC)")


def check_if_can_learn(ctx):
    """Can learn: ravenkeeper"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.ravenkeeper.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use learn command (BoTC)")


def check_if_can_read(ctx):
    """Can read: fortune teller"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.fortuneteller.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use read command (BoTC)")


def check_if_can_kill(ctx):
    """Can kill: imp"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.imp.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use kill command (BoTC)")


def check_if_can_slay(ctx):
    """Can slay: slayer"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.slayer.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use slay command (BoTC)")


def check_if_can_protect(ctx):
    """Can protect: monk"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.role.ego_self.name in [TBRole.monk.value]:
        return True
    else:
        raise RoleCannotUseCommand("Cannot use protect command (BoTC)")


def check_if_is_night(ctx):
    """Check if the game is in night phase"""
    import globvars
    return globvars.master_state.game.is_night()


def check_if_is_day(ctx):
    """Check if the game is in day phase"""
    import globvars
    return globvars.master_state.game.is_day()


def check_if_dm(ctx):
    """Check if the command is invoked in a dm channel."""
    return ctx.guild is None


def check_if_lobby(ctx):
    """Check if the command is invoked in the lobby."""
    return ctx.channel.id == int(LOBBY_CHANNEL_ID)


def check_if_player_alive(ctx):
    """Check if the player is alive using apparent state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    return player.is_apparently_alive()


def check_if_player_dead(ctx):
    """Check if the player is dead using apparent state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    return player.is_apparently_dead()


class BoTCCommands(commands.Cog, name="BoTC in-game commands"):
    """BoTC in-game commands cog
    (privilege one unique command keyword per character ability)

    Ability commands:
    - serve: butler
    - poison: poisoner
    - learn: ravenkeeper
    - read: fortune teller
    - kill: imp
    - slay: slayer
    - protect: monk

    Day commands:
    - nominate
    - yes
    - no
    """
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check performed on all commands of this cog.
        Must be a non-fleaved player to use these commands.
        """
        return check_if_is_player(ctx)
    

    # ---------- SERVE COMMAND (Butler) ----------------------------------------
    @commands.command(pass_context=True, name = "serve")
    @commands.check(check_if_can_serve)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def serve(self, ctx, *, master: PlayerParser()):
        """Serve command: 
        usage: serve <player> and <player> and...
        characters: butler
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_serve(master)

    @serve.error
    async def serve_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- POISON COMMAND (Poisoner) ----------------------------------------
    @commands.command(pass_context=True, name = "poison")
    @commands.check(check_if_can_poison)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def poison(self, ctx, *, poisoned: PlayerParser()):
        """Poison command
        usage: poison <player> and <player> and...
        characters: poisoner
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_poison(poisoned)

    @poison.error
    async def poison_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- LEARN COMMAND (Ravenkeeper) ----------------------------------------
    @commands.command(pass_context=True, name = "learn")
    @commands.check(check_if_can_learn)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def learn(self, ctx, *, learned: PlayerParser()):
        """Learn command
        usage: learn <player> and <player> and...
        characters: ravenkeeper
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_learn(learned)

    @learn.error
    async def learn_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- READ COMMAND (Fortune Teller) ----------------------------------------
    @commands.command(pass_context=True, name = "read")
    @commands.check(check_if_can_read)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def read(self, ctx, *, read: PlayerParser()):
        """Read command
        usage: read <player> and <player> and...
        characters: fortune teller
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_read(read)

    @read.error
    async def read_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- KILL COMMAND (Imp) ----------------------------------------
    @commands.command(pass_context=True, name = "kill")
    @commands.check(check_if_can_kill)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def kill(self, ctx, *, killed: PlayerParser()):
        """Kill command
        usage: kill <player> and <player> and...
        characters: imp
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_kill(killed)

    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- SLAY COMMAND (Slayer) ----------------------------------------
    @commands.command(pass_context=True, name = "slay")
    @commands.check(check_if_can_slay)
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    @commands.check(check_if_player_alive)
    async def slay(self, ctx, *, slain: PlayerParser()):
        """Slay command
        usage: slay <player> and <player> and...
        characters: slayer
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_slay(slain)

    @slay.error
    async def slay_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- PROTECT COMMAND (Monk) ----------------------------------------
    @commands.command(pass_context=True, name = "protect")
    @commands.check(check_if_can_protect)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def protect(self, ctx, *, protected: PlayerParser()):
        """Protect command
        usage: protect <player> and <player> and...
        characters: monk
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        player.role.ego_self.exec_protect(protected)

    @protect.error
    async def protect_error(self, ctx, error):
        if isinstance(error, RoleCannotUseCommand):
            return
        elif isinstance(error, NotAPlayer):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
    

    # ---------- NOMINATE COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "nominate", aliases = ["nom", "nomination"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def nominate(self, ctx, *, nominated: PlayerParser()):
        """Nominate command
        usage: nominate <player> and <player> and...
        characters: living players
        """
        pass

    @nominate.error
    async def nominate_error(self, ctx, error):
        try:
            raise error
        except Exception:
            await ctx.send(error_str)
            await botutils.log(botutils.Level.error, traceback.format_exc()) 

    
    # ---------- YES COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "yes", aliases = ["y", "ye", "yay"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def yes(self, ctx):
        """Yes command
        usage: yes
        characters: all players
        """
        pass

    @yes.error
    async def yes_error(self, ctx, error):
        try:
            raise error
        except Exception:
            await ctx.send(error_str)
            await botutils.log(botutils.Level.error, traceback.format_exc()) 
    

    # ---------- NO COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "no", aliases = ["n", "nay", "nope"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def no(self, ctx):
        """No command
        usage: no
        characters: all players
        """
        pass

    @no.error
    async def no_error(self, ctx, error):
        try:
            raise error
        except Exception:
            await ctx.send(error_str)
            await botutils.log(botutils.Level.error, traceback.format_exc()) 

    
def setup(client):
    client.add_cog(BoTCCommands(client))
