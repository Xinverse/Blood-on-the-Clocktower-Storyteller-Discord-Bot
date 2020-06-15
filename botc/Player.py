"""Contains the Player class"""

from .PlayerState import PlayerState


class Player:
    """Player class"""

    def __init__(self, user_obj, role_obj):
        self._user_obj = user_obj  # Discord user object
        self._role_obj = role_obj  # Role object
        self._state_obj = PlayerState.alive  # Enum object

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
