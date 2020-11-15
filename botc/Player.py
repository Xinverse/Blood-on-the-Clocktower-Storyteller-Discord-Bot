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
        self.ghost_vote = 1
        self.has_nominated = False
        self.was_nominated = False
    
    def toggle_has_nominated(self):
        """The player has nominated a person."""
        self.has_nominated = True
    
    def can_nominate(self):
        """Can this player nominate?"""
        return not self.has_nominated
    
    def toggle_was_nominated(self):
        """The player has been nominated"""
        self.was_nominated = True
    
    def can_be_nominated(self):
        """Can this player be nominated?"""
        return not self.was_nominated
    
    def reset_nomination(self):
        """Call this function at the end of each day to reset nomination data"""
        self.has_nominated = False
        self.was_nominated = False
    
    async def exec_change_role(self, new_role):
        """Change the player's old role to a new role"""
        import globvars
        self._role_obj = new_role
        await globvars.master_state.game.check_winning_conditions()
    
    async def exec_real_death(self, modkill=False):
        """Turn the player's real state into the death state"""
        import globvars
        if self.is_dead():
            raise AlreadyDead("Player is already dead, you are trying to kill them again.")
        if modkill:
            self._state_obj = PlayerState.fleaved
            self._apparent_state_obj = PlayerState.fleaved
        else:
            self._state_obj = PlayerState.dead
            self._apparent_state_obj = PlayerState.dead
        await botutils.add_dead_role(self.user)
        await botutils.remove_alive_role(self.user)
        await globvars.master_state.game.check_winning_conditions()
    
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
    
    def spend_vote(self):
        """Spend a vote after a vote has been cast by the player"""
        # An alive player has infinite votes
        if self.is_apparently_alive():
            return
        # A dead player has only one ghost vote.
        else:
            assert self.ghost_vote, f"{self.game_nametag} ghost vote has been spent."
            self.ghost_vote -= 1
    
    def has_vote(self):
        """Retrun True if the player is able to vote. False otherwise."""
        # An alive player has infinite votes
        if self.is_apparently_alive():
            return True
        # A dead player has only one ghost vote
        else:
            return self.ghost_vote

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
