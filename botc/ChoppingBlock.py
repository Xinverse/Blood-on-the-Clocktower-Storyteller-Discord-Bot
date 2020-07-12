"""Contains the Chopping Block class"""

class ChoppingBlock:
    """A class to store data about which player was about to be lynched, 
    and by how many votes
    """

    def __init__(self, player, nb_votes):
        """
        Parameters

        @player :  Player object. The player that is about to be lynched.
        @nb_votes : Integer. The number of "yes" votes (raised hands) on that player.
        """
        self.player_about_to_die = player
        self.nb_votes = nb_votes
        