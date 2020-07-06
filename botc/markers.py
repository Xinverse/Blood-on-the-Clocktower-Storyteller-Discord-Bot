"""Contains the MarkerGrib class"""


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


class MarkerGrid:
    """A calendar like grid to keep track of markers (special tags) for player ability
    [
        night1, dawn1, day1,
        night2, dawn2, day3,
        etc.
    ]
    """

    def __init__(self):
        self.grid = _GrowingList()
    
    def register_a_reminder(self, action, phase_id):
        """Save a marker within the grid based on a phase ID"""
        self.grid[phase_id] = action
    
    def retrieve_a_reminder(self, phase_id):
        """Retrieve a marker within the grid based on a phase ID"""
        return self.grid[phase_id]
        