"""Contains the Role Guide class"""

class RoleGuide:
    """Role Guide class: provides the number of each category of characters given 
    the total number of players
    """

    GUIDE = {
        # p = number of players
        # t = number of townsfolks
        # o = number of outsiders
        # m = number of minions
        # d = number of demons

        #p     t  o  m  d
        '5' : [3, 0, 1, 1],
        '6' : [3, 1, 1, 1],
        '7' : [5, 0, 1, 1],
        '8' : [5, 1, 1, 1],
        '9' : [5, 2, 1, 1],
        '10': [7, 0, 2, 1],
        '11': [7, 1, 2, 1],
        '12': [7, 2, 2, 1],
        '13': [9, 0, 3, 1],
        '14': [9, 1, 3, 1],
        '15': [9, 2, 3, 1]
    }

    def __init__(self, nb_players: int):

        self._nb_players = nb_players
        role_guide_chart = RoleGuide.GUIDE[str(nb_players)]
        self._nb_townsfolks = role_guide_chart[0]
        self._nb_outsiders = role_guide_chart[1]
        self._nb_minions = role_guide_chart[2]
        self._nb_demons = role_guide_chart[3]

    @property
    def nb_players(self):
        return self._nb_players

    @property
    def nb_townsfolks(self):
        return self._nb_townsfolks

    @property
    def nb_outsiders(self):
        return self._nb_outsiders

    @property
    def nb_minions(self):
        return self._nb_minions

    @property
    def nb_demons(self):
        return self._nb_demons
    