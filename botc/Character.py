"""Contains the Character class"""

class Character:
    """Character class"""
    
    def __init__(self):
        self._role_enum = None

    @property
    def name(self):
        return self._role_enum.value