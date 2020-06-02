"""Contains a dummy game class for testing purposes"""

from botutils import GameMeta

class TestGame(GameMeta):
    """A dummy game class for testing purposes"""

    def __init__(self):
        pass

    def register_players(self, id_list):
        pass

    def start_game(self):
        pass

    def end_game(self):
        pass

    @property
    def phase(self):
        pass
    