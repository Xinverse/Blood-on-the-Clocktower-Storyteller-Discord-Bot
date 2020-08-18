"""Contains the bot global state"""

import enum

class BotState(enum.Enum):
    """Bot global state class:
    empty: The lobby is completely empty
    pregame: The lobby is filled but no game is going on
    game: A game is currently in session
    """

    empty = "empty"
    pregame = "pregame"
    game = "game"

