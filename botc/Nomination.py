"""Contains the Nomination class"""

class Nomination:
    """Nomination class"""

    def __init__(self, nominator_player_obj, nominated_player_obj):
        self._nominator = nominator_player_obj  # Player object
        self._nominated = nominated_player_obj  # Player object
    
    @property
    def nominator(self):
        return self._nominator
    
    @property
    def nominated(self):
        return self._nominated