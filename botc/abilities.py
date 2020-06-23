"""Contains the action class for botc night/day character abilities"""

import enum


class ActionTypes(enum.Enum):
    """Ability commands:
    - serve: butler
    - poison: poisoner
    - learn: ravenkeeper
    - read: fortune teller
    - kill: imp
    - slay: slayer
    - protect: monk
    """

    serve = "serve"
    poison = "poison"
    learn = "learn"
    read = "read"
    kill = "kill"
    slay = "slay"
    protect = "protect"


class Action:
    """Action class to represent character ability"""

    def __init__(self, source_player, target_player, action_type):
        self.source_player = source_player
        self.target_player = target_player
        self.action_type = action_type
