"""Contains classes about BoTC in-game status effects"""

import enum

DEFAULT_EFFECT_DURATION = 3


class StatusList(enum.Enum):
   """List of status effects in game"""

   safety_from_demon = "safe_from_demon"
   drunkenness = "drunkenness"
   poison = "poisoned"
   red_herring = "red_herring"
   under_service = "under_service"


class Storyteller:
    """Storyteller class. Used to indicate sources of certain effects."""
    pass


class StatusEffect:
    """Parent class for status effect."""

    def __init__(self, source_player, affected_player, duration):
        """Initalize the object.

        Param:
        source_player: Player responsible for the status effect infliction. 
                       It's Storyteller() if it's an effect inflicted by the storyteller.
        affected_player: Player affected by the status effect.
        duration: The number of phases the effect will last for. (3 phases mean the night
                  when the effect was inflicted, the next dawn, and the next day.)
        """
        self.source_player = source_player
        self.affected_player = affected_player
        self.duration = duration
        self.__is_active = None
        self.__effect = None
    
    def __repr__(self):
        return f"Status {self.__effect} on {self.affected_player}"
    
    def wear_off(self):
        """Wear off the effect duration by 1 phase"""
        self.duration -= 1
    
    def manually_enable(self):
        """Manually enable the effect"""
        self.__is_active = True
    
    def manually_disable(self):
        """Manually disable the effect"""
        self.__is_active = False
    
    def is_active(self):
        """Return True if the status effect is active, false otherwise. 
        Manual enabling and disabling have precedence over duration wearing off.
        """
        if self.__is_active is not None:
            return self.__is_active
        return self.duration > 0
    
    @property
    def effect(self):
        """Return the enum value of the effect"""
        if self.__effect:
            return self.__effect
        else:
            print(self.__repr__())
            raise NotImplementedError


class SafetyFromDemon(StatusEffect):
    """Safety from demon effect. Affected player will not die from demon kill."""

    def __init__(self, source_player, affected_player, duration = DEFAULT_EFFECT_DURATION):
        super().__init__(source_player, affected_player, duration)
        self.__effect = StatusList.safety_from_demon


class Drunkenness(StatusEffect):
    """Drunkenness effect"""

    def __init__(self, source_player, affected_player, duration = DEFAULT_EFFECT_DURATION):
        super().__init__(source_player, affected_player, duration)
        self.__effect = StatusList.drunkenness


class Poison(StatusEffect):
    """Poison effect"""

    def __init__(self, source_player, affected_player, duration = DEFAULT_EFFECT_DURATION):
        super().__init__(source_player, affected_player, duration)
        self.__effect = StatusList.poison


class RedHerring(StatusEffect):
    """Red herring for the fortune teller character."""

    def __init__(self, source_player, affected_player, duration = 1000000):
        """The red herring effect lasts the whole game, so we initialize it with 
        a really large number
        """
        super().__init__(source_player, affected_player, duration)
        self.__effect = StatusList.red_herring
