"""Contains the Player class"""

import botutils
from .PlayerState import PlayerState
from .abilities import ActionGrid
from .errors import AlreadyDead


class Player:
    """Player class
    
    State: the real life/death state of the player
    Apparent state: the apparent life/death state of the player (ex. Zombuul)

    (Fleaved must be a real state as it pertains to game participation.)
    """

    def __init__(self, user_obj, role_obj):
        self._user_obj = user_obj  # Discord user object
        self._role_obj = role_obj  # Role object
        self._state_obj = PlayerState.alive  # Enum object
        self._apparent_state_obj = PlayerState.alive  # Enum object
        self.action_grid = ActionGrid()  # ActionGrib object
        self._status_effects = []  # List object
    
    def exec_change_role(self, new_role):
        """Change the player's old role to a new role"""
        self._role_obj = new_role
    
    async def exec_real_death(self):
        """Turn the player's real state into the death state"""
        if self.is_dead():
            raise AlreadyDead("Player is already dead, you are trying to kill them again.")
        self._state_obj = PlayerState.dead
        self._apparent_state_obj = PlayerState.dead
        await botutils.add_dead_role(self.user)
        await botutils.remove_alive_role(self.user)
    
    async def exec_apparent_death(self):
        """Turn the player's apparent state into the death state, but the real state 
        remains alive
        """
        if self.is_apparently_dead():
            raise AlreadyDead("Player is already 'apparently' dead, you are trying to " \
                "kill them again.")
        self._apparent_state_obj = PlayerState.dead
        await botutils.add_dead_role(self.user)
        await botutils.remove_alive_role(self.user)
    
    def has_status_effect(self, status_effect):
        """Check if a player has a status effect"""
        return status_effect in \
            [status.effect for status in self.status_effects if status.is_active()]
    
    def is_droisoned(self):
        """Return true if the player is currently drunk or poisoned (droison) when the 
        check is performed, false otherwise.
        """
        from botc.gamemodes.troublebrewing import Drunk
        from botc import StatusList
        # The player's true role is Drunk
        if self.role.true_self.name == Drunk().name:
            return True
        # The player is affected by an active poison effect
        elif StatusList.poison in \
            [status.effect for status in self.status_effects if status.is_active()]:
            return True
        # The player is affected by an active drunkenness effect
        elif StatusList.drunkenness in \
            [status.effect for status in self.status_effects if status.is_active()]:
            return True
        return False
    
    def add_status_effect(self, new_status_effect):
        """Add a status effect"""
        self._status_effects.append(new_status_effect)
    
    def is_apparently_alive(self):
        return self.apparent_state == PlayerState.alive
    
    def is_apparently_dead(self):
        return self.apparent_state == PlayerState.dead
    
    def is_alive(self):
        return self.state == PlayerState.alive
    
    def is_dead(self):
        return self.state == PlayerState.dead

    def is_fleaved(self):
        return self.state == PlayerState.fleaved
    
    @property
    def game_nametag(self):
        """Return a nicely formatted name for the player."""
        return f"**{self.user.display_name}** `({self.user.id})`"

    @property
    def user(self):
        return self._user_obj
    
    @property
    def userid(self):
        return self._user_obj.id
    
    @property
    def role(self):
        return self._role_obj
    
    @property
    def state(self):
        return self._state_obj

    @property
    def apparent_state(self):
        return self._apparent_state_obj
    
    @property
    def status_effects(self):
        return self._status_effects

    def __repr__(self):
        return f"{str(self.user.display_name)} ({self.user.id}) is {str(self.role)}"
    
    def __str__(self):
        return self.__repr__()
