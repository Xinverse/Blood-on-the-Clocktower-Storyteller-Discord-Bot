"""Contains the cog for BoTC in-game commands"""

import configparser
import botutils
import traceback
import json
import globvars
from discord.ext import commands
from botc import BOTCUtils, NotAPlayer, PlayerParser, RoleCannotUseCommand, NotDMChannel, \
    NotLobbyChannel, NotDay, NotNight, DeadOnlyCommand, AliveOnlyCommand
from botc.gamemodes.troublebrewing._utils import TBRole

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)


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
    if globvars.master_state.game.is_night():
        return True
    else:
        raise NotNight("Command is allowed during night phase only (BoTC)")


def check_if_is_day(ctx):
    """Check if the game is in day phase"""
    import globvars
    if globvars.master_state.game.is_day():
        return True
    else:
        raise NotDay("Command is allowed during day phase only (BoTC)")


def check_if_dm(ctx):
    """Check if the command is invoked in a dm channel."""
    if ctx.guild is None:
        return True
    else:
        raise NotDMChannel("Only DM allowed (BoTC)")


def check_if_lobby(ctx):
    """Check if the command is invoked in the lobby."""
    if ctx.channel.id == int(LOBBY_CHANNEL_ID):
        return True
    else:
        raise NotLobbyChannel("Only lobby allowed (BoTC)")


def check_if_player_apparently_alive(ctx):
    """Check if the player is alive using apprent state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.is_apparently_alive():
        return True
    else:
        raise AliveOnlyCommand("Command reserved for Alive Players (BoTC)")


def check_if_player_apparently_dead(ctx):
    """Check if the player is dead using apparent state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.is_apparently_dead():
        return True
    else:
        raise DeadOnlyCommand("Command reserved for Dead Players (BoTC)")


def check_if_player_really_alive(ctx):
    """Check if the player is alive using real state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.is_alive():
        return True
    else:
        raise AliveOnlyCommand("Command reserved for Alive Players (BoTC)")


def check_if_player_really_dead(ctx):
    """Check if the player is dead using real state"""
    player = BOTCUtils.get_player_from_id(ctx.author.id)
    if player.is_dead():
        return True
    else:
        raise DeadOnlyCommand("Command reserved for Dead Players (BoTC)")


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
        return check_if_is_player(ctx)  # Registered non-quit player -> NotAPlayer
    

    # ---------- SERVE COMMAND (Butler) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "serve",
        hidden = True,
        brief = documentation["doc"]["serve"]["brief"],
        help = documentation["doc"]["serve"]["help"],
        description = documentation["doc"]["serve"]["description"]
    )
    @commands.check(check_if_can_serve)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def serve(self, ctx, *, master: PlayerParser()):
        """Serve command: 
        usage: serve <player> and <player> and...
        characters: butler
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_serve(master)

    @serve.error
    async def serve_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- POISON COMMAND (Poisoner) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "poison",
        hidden = True,
        brief = documentation["doc"]["poison"]["brief"],
        help = documentation["doc"]["poison"]["help"],
        description = documentation["doc"]["poison"]["description"]
    )
    @commands.check(check_if_can_poison)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def poison(self, ctx, *, poisoned: PlayerParser()):
        """Poison command
        usage: poison <player> and <player> and...
        characters: poisoner
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_poison(poisoned)

    @poison.error
    async def poison_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- LEARN COMMAND (Ravenkeeper) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "learn",
        hidden = True,
        brief = documentation["doc"]["learn"]["brief"],
        help = documentation["doc"]["learn"]["help"],
        description = documentation["doc"]["learn"]["description"]
    )
    @commands.check(check_if_can_learn)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_dead)  # Player dead -> DeadOnlyCommand
    async def learn(self, ctx, *, learned: PlayerParser()):
        """Learn command
        usage: learn <player> and <player> and...
        characters: ravenkeeper
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_learn(learned)

    @learn.error
    async def learn_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not dead -> DeadOnlyCommand
        elif isinstance(error, DeadOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["dead_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- READ COMMAND (Fortune Teller) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "read",
        hidden = True,
        brief = documentation["doc"]["read"]["brief"],
        help = documentation["doc"]["read"]["help"],
        description = documentation["doc"]["read"]["description"]
    )
    @commands.check(check_if_can_read)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def read(self, ctx, *, read: PlayerParser()):
        """Read command
        usage: read <player> and <player> and...
        characters: fortune teller
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_read(read)

    @read.error
    async def read_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- KILL COMMAND (Imp) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "kill",
        brief = documentation["doc"]["kill"]["brief"],
        help = documentation["doc"]["kill"]["help"],
        description = documentation["doc"]["kill"]["description"]
    )
    @commands.check(check_if_can_kill)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def kill(self, ctx, *, killed: PlayerParser()):
        """Kill command
        usage: kill <player> and <player> and...
        characters: imp
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_kill(killed)

    @kill.error
    async def kill_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- SLAY COMMAND (Slayer) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "slay",
        hidden = True,
        brief = documentation["doc"]["slay"]["brief"],
        help = documentation["doc"]["slay"]["help"],
        description = documentation["doc"]["slay"]["description"]
    )
    @commands.check(check_if_can_slay)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_lobby)  # Correct channel -> NotLobbyChannel
    @commands.check(check_if_is_day)  # Correct phase -> NotDay
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def slay(self, ctx, *, slain: PlayerParser()):
        """Slay command
        usage: slay <player> and <player> and...
        characters: slayer
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_slay(slain)

    @slay.error
    async def slay_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotLobbyChannel):
            await ctx.author.send(documentation["cmd_warnings"]["lobby_only"].format(ctx.author.mention, emoji))
        # Incorrect phase -> NotDay
        elif isinstance(error, NotDay):
            await ctx.author.send(documentation["cmd_warnings"]["day_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 


    # ---------- PROTECT COMMAND (Monk) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "protect",
        hidden = True,
        brief = documentation["doc"]["protect"]["brief"],
        help = documentation["doc"]["protect"]["help"],
        description = documentation["doc"]["protect"]["description"]
    )
    @commands.check(check_if_can_protect)  # Correct character -> RoleCannotUseCommand
    @commands.check(check_if_dm)  # Correct channel -> NotDMChannel
    @commands.check(check_if_is_night)  # Correct phase -> NotNight
    @commands.check(check_if_player_really_alive)  # Player alive -> AliveOnlyCommand
    async def protect(self, ctx, *, protected: PlayerParser()):
        """Protect command
        usage: protect <player> and <player> and...
        characters: monk
        """
        player = BOTCUtils.get_player_from_id(ctx.author.id)
        await player.role.ego_self.exec_protect(protected)

    @protect.error
    async def protect_error(self, ctx, error):
        emoji = documentation["cmd_warnings"]["x_emoji"]
        # Incorrect character -> RoleCannotUseCommand
        if isinstance(error, RoleCannotUseCommand):
            return
        # Non-registered or quit player -> NotAPlayer
        elif isinstance(error, NotAPlayer):
            return
        # Incorrect channel -> NotDMChannel
        elif isinstance(error, NotDMChannel):
            return
        # Incorrect phase -> NotNight
        elif isinstance(error, NotNight):
            await ctx.author.send(documentation["cmd_warnings"]["night_only"].format(ctx.author.mention, emoji))
        # Player not alive -> AliveOnlyCommand
        elif isinstance(error, AliveOnlyCommand):
            await ctx.author.send(documentation["cmd_warnings"]["alive_only"].format(ctx.author.mention, emoji))
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 
    

    # ========== NOMINATE COMMAND (Voting) ==============================
    @commands.command(
        pass_context = True, 
        name = "nominate", 
        aliases = ["nom", "nomination"]
    )
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    @commands.check(check_if_player_apparently_alive)
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
    @commands.command(
        pass_context = True, 
        name = "yes", 
        aliases = ["y", "ye", "yay"]
    )
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
    @commands.command(
        pass_context = True, 
        name = "no", 
        aliases = ["n", "nay", "nope"]
    )
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
