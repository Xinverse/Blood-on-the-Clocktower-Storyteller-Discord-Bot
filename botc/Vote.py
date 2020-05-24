"""Contains the Vote class"""

class Vote:
    """Vote class"""

    def __init__(self, voter_player_obj, ballot_obj):
        self._voter = voter_player_obj  # Player object
        self._ballot = ballot_obj  # Ballot object
    
    @property
    def voter(self):
        return self._voter

    @property
    def ballot(self):
        return self._ballot
