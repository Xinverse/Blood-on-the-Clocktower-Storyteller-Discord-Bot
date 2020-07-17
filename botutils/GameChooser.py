"""Contains the GameChooser class"""

class GameChooser:
    """A class to faciliate gamemode choosing and voting"""

    from botc.Game import Game
    
    _default_game = Game()

    @property
    def default_game(self):
        return self._default_game
    
    def get_selected_game(self):
        return self._default_game
