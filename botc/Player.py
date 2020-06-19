"""Contains the Player class"""

from .PlayerState import PlayerState


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
