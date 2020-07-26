"""Contains classes about BoTC in-game status effects"""

import enum

DEFAULT_EFFECT_DURATION = 3


class StatusList(enum.Enum):
   """List of status effects in game"""

   safety_from_demon = "safe_from_demon"
   drunkenness = "drunkenness"
   poison = "poisoned"
   red_herring = "red_herring"
   butler_service = "butler_service"  # butler serving a master
   ravenkeeper_activated = "ravenkeeper_activated"  # activated ravenkeeper ability


class Storyteller:
    """Storyteller class. Used to indicate sources of certain effects."""
    pass


class StatusEffect:
    """Parent class for status effect."""

    def __init__(self, source_player, affected_player, pointer_player, duration):
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
        self.pointer_player = pointer_player
        self.duration = duration
        self._is_active = None
        self._effect = None
    
    def __repr__(self):
        return f"Status {self._effect} on {self.affected_player}"
    
    def wear_off(self):
        """Wear off the effect duration by 1 phase"""
        self.duration -= 1
    
    def manually_enable(self):
        """Manually enable the effect"""
        self._is_active = True
    
    def manually_disable(self):
        """Manually disable the effect"""
        self._is_active = False
    
    def is_active(self):
        """Return True if the status effect is active, false otherwise. 
        Manual enabling and disabling have precedence over duration wearing off.
        """
        if self._is_active is not None:
            return self._is_active
        return self.duration > 0
    
    @property
    def effect(self):
        """Return the enum value of the effect"""
        if self._effect:
            return self._effect
        else:
            raise NotImplementedError


class RavenkeeperActivated(StatusEffect):
    """Ravenkeerper ability is active."""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player = None, 
            duration = 2
        ):
        """
        @source_player : the ravenkeeper
        @affected_player : the ravenkeeper
        @pointer_player : None
        @duration : 2 phases (the same night, next dawn)
        """
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.ravenkeeper_activated


class SafetyFromDemon(StatusEffect):
    """Safety from demon effect. Affected player will not die from demon kill."""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player = None, 
            duration = DEFAULT_EFFECT_DURATION
        ):
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.safety_from_demon


class Drunkenness(StatusEffect):
    """Drunkenness effect"""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player = None,
            duration = DEFAULT_EFFECT_DURATION
        ):
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.drunkenness


class Poison(StatusEffect):
    """Poison effect"""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player = None, 
            duration = DEFAULT_EFFECT_DURATION
        ):
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.poison


class RedHerring(StatusEffect):
    """Red herring for the fortune teller character."""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player = None, 
            duration = 1000000
        ):
        """The red herring effect lasts the whole game, so we initialize it with 
        a really large number
        """
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.red_herring
    

class ButlerService(StatusEffect):
    """Butler under service of a master"""

    def __init__(
            self, 
            source_player, 
            affected_player, 
            pointer_player, 
            duration = DEFAULT_EFFECT_DURATION
        ):
        """
        @source_player : the butler
        @affected_player : the butler
        @pointer_player : the master
        @duration : 3 phases by default (the same night, next dawn, and next day)
        """
        super().__init__(source_player, affected_player, pointer_player, duration)
        self._effect = StatusList.butler_service
