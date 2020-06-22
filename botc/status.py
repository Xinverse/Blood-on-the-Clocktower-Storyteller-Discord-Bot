"""Contains classes about BoTC in-game status effects"""

import enum


class StatusList(enum.Enum):
   """List of status effects in game"""

   safety_from_demon = "safe_from_demon"
   drunkenness = "drunkenness"
   poison = "poisoned"
   red_herring = "red_herring"


class Storyteller:
    """Storyteller class. Used to indicate sources of certain effects."""
    pass


class StatusEffect:
    """Parent class for status effect."""

    def __init__(self, source_player, affected_player):
        """Initalize the object.

        Param:
        source_player: Player responsible for the status effect infliction. 
                       It's Storyteller() if it's an effect inflicted by the storyteller.
        affected_player: Player affected by the status effect.
        """
        self.source_player = source_player
        self.affected_player = affected_player
        self.is_active = True
        self.__effect = None
    
    def enable(self):
        self.is_active = True
    
    def disable(self):
        self.is_active = False
    
    @property
    def effect(self):
        if self.__effect:
            return self.__effect
        else:
            raise NotImplementedError


class SafetyFromDemon(StatusEffect):
    """Safety from demon effect. Affected player will not die from demon kill."""

    def __init__(self, source_player, affected_player):
        super().__init__(source_player, affected_player)
        self.__effect = StatusList.safety_from_demon


class Drunkenness(StatusEffect):
    """Drunkenness effect"""

    def __init__(self, source_player, affected_player):
        super().__init__(source_player, affected_player)
        self.__effect = StatusList.drunkenness


class Poison(StatusEffect):
    """Poison effect"""

    def __init__(self, source_player, affected_player):
        super().__init__(source_player, affected_player)
        self.__effect = StatusList.poison


class RedHerring(StatusEffect):
    """Red herring for the fortune teller character."""

    def __init__(self, source_player, affected_player):
        super().__init__(source_player, affected_player)
        self.__effect = StatusList.red_herring
