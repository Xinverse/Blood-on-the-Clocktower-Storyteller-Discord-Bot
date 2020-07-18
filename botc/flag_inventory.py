"""Contains the character based inventory system"""

import enum


class Flags(enum.Enum):

    slayer_unique_attempt = "slayer_unique_attempt"
    virgin_first_nomination = "virgin_first_nomination"


class Inventory:
    """Inventory class

    This class represents a character's inventory. The inventory contains 
    flags that will be spent after usage, in order to keep track of unique 
    and/or special abilities.
    """

    def __init__(self, *args):
        """Initialize with a series of flag objects"""
        self.inv = list(args)
    
    def __repr__(self):
        return str(self.inv)
    
    def has_item_in_inventory(self, item):
        """Check if an item is in the inventory. The item must be of the Flag() type."""
        return item in self.inv
    
    def add_item_to_inventory(self, new_item):
        """Add a new flag into the inventory. The item must be of the Flag() type."""
        self.inv.append(new_item)

    def remove_item_from_inventory(self, item_to_remove):
        """Remove a new flag from the inventory. The item must be of the Flag() type."""
        self.inv.remove(item_to_remove)
