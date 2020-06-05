"""Example game pack:
Required file: Game.py

Contains the Game() class that runs the game.
"""

from models import GameMeta

class Game(GameMeta):
    """Game class that runs the game"""
    
    def register_players(self, id_list):
        """Register the players. This method must be implemented"""
        pass

    
    def start_game(self):
        """Start the game. This method must be implemented"""
        pass

    
    def end_game(self):
        """End the game, compute winners etc. This method must be implemented"""
        pass

    
    def phase(self):
        """Return the current phase the game is in (day, night, etc.) This method must be implemented."""
        pass
    