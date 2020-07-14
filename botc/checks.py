"""Contains some checking functions for botc commands"""

import configparser
from botc import BOTCUtils, NotAPlayer, RoleCannotUseCommand, AliveOnlyCommand, \
    DeadOnlyCommand, NotDay, NotDawn, NotNight, NotDMChannel, NotLobbyChannel

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]


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


def can_use_serve(user_id):
    """Return true if the user can use the command "serve"
    Characters that can serve: 
    - Butler
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.butler.value]:
        return True
    return False


def check_if_can_serve(ctx):
    """Return true if the command user can use the command "serve"
    Command check function
    """
    if can_use_serve(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use serve command (BoTC)")


def can_use_poison(user_id):
    """Return true if the user can use the command "poison"
    Characters that can poison:
    - Poisoner
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.poisoner.value]:
        return True
    return False


def check_if_can_poison(ctx):
    """Return true if the command user can use the command "poison"
    Command check function
    """
    if can_use_poison(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use poison command (BoTC)")


def can_use_learn(user_id):
    """Return true if the user can use the command "poison"
    Characters that can poison:
    - Ravenkeeper
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.ravenkeeper.value]:
        return True
    return False


def check_if_can_learn(ctx):
    """Return true if the command user can use the command "learn"
    Command check function
    """
    if can_use_learn(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use learn command (BoTC)")


def can_use_read(user_id):
    """Return true if the user can use the command "read"
    Characters that can poison:
    - Fortune teller
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.fortuneteller.value]:
        return True
    return False


def check_if_can_read(ctx):
    """Return true if the command user can use the command "read"
    Command check function
    """
    if can_use_read(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use read command (BoTC)")


def can_use_kill(user_id):
    """Return true if the user can use the command "kill"
    Characters that can poison:
    - Imp
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.imp.value]:
        return True
    return False


def check_if_can_kill(ctx):
    """Return true if the command user can use the command "kill"
    Command check function
    """
    if can_use_kill(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use kill command (BoTC)")


def can_use_slay(user_id):
    """Return true if the user can use the command "slay"
    Characters that can slay:
    - All characters (to allow for fake claiming)
    """
    return True


def check_if_can_slay(ctx):
    """Return true if the command user can use the command "slay"
    Command check function
    """
    if can_use_slay(ctx.author.id):
        return True
    else:
        raise RoleCannotUseCommand("Cannot use slay command (BoTC)")


def can_use_protect(user_id):
    """Return true if the user can use the command "protect"
    Characters that can poison:
    - Monk
    """
    from botc.gamemodes.troublebrewing._utils import TBRole
    player = BOTCUtils.get_player_from_id(user_id)
    if player.role.ego_self.name in [TBRole.monk.value]:
        return True
    return False


def check_if_can_protect(ctx):
    """Return true if the command user can use the command "protect"
    Command check function
    """
    if can_use_protect(ctx.author.id):
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


def check_if_is_dawn(ctx):
    """Check if the game is in dawn phase"""
    import globvars
    if globvars.master_state.game.is_dawn():
        return True
    else:
        raise NotDawn("Command is allowed during dawn phase only (BoTC")


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
