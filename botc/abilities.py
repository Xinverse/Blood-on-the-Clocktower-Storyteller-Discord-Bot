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
    assassinate = "assassinate"


class Action:
    """Action class to represent character ability"""

    def __init__(self, source_player, target_player, action_type, phase_id):
        """Param:
        @source_player : player that did the action (Player() object)
        @target_player : player or players targetted by the action (Target() object)
        @action_type : enum object describing the action (see above)
        @birth_phase_id : the phase ID when it was registered
        """
        self.source_player = source_player
        self.target_player = target_player
        self.action_type = action_type
        self.birth_phase_id = phase_id
    
    def __repr__(self):

        return f"Action {self.action_type}"


class _GrowingList(list):
    """A list that grows automatically when an index that does not exist yet is referenced, 
    filling the rest of the values with filler items
    """

    def __setitem__(self, index, value):
        """Set item
        If list is not long enough, grow it and fill with default None value.
        """
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
    
    def __getitem__(self, index):
        """Get item
        If list is not long enough, don't grow and return None.
        """
        if index >= len(self):
            return None
        return list.__getitem__(self, index)


class ActionGrid:
    """A calendar like grid to keep track of actions (abilities) used by players
    [
        night1, dawn1, day1,
        night2, dawn2, day3,
        etc.
    ]
    """

    def __init__(self):
        self.grid = _GrowingList()
    
    def register_an_action(self, action, phase_id):
        """Save an action within the grid based on a phase ID"""
        self.grid[phase_id] = action
    
    def retrieve_an_action(self, phase_id):
        """Retrieve an action within the grid based on a phase ID"""
        return self.grid[phase_id]
