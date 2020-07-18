"""Contains the Master State Machine"""

import time
from .Pregame import Pregame
from .BotState import BotState


class State:
    """State class
    """

    def run(self, master):
        assert 0, "run() method not implemented"

    def update(self, master):
        assert 0, "next() method not implemented"


class PregameState(State):
    """Pregame state/phase: 
    When some players have joined in the lobby, but the game has not started yet
    """

    def run(self, master):
        print("Current state in the PREGAME phase.")
        master.transition_to_pregame()
    
    def update(self, master):
        if master.game:
            master.transition_to_game()
            return GameState()
        elif master.pregame.is_empty():
            master.transition_to_empty()
            return EmptyState()
        else:
            return PregameState()


class GameState(State):
    """Game state/phase
    When a game is going on in the lobby.
    """

    def run(self, master):
        print("Current state in the GAME phase.")
        master.transition_to_game()
    
    def update(self, master):
        if master.game:
            return GameState()
        else:
            master.transition_to_empty()
            return EmptyState()


class EmptyState(State):
    """Empty state/phase
    When the lobby is entirely empty and no player has joined.
    """

    def run(self, master):
        print("Current state in the EMPTY phase.")
        master.transition_to_empty()
    
    def update(self, master):
        if not master.pregame.is_empty():
            master.transition_to_pregame()
            return PregameState()
        else:
            return EmptyState()


class StateMachine:
    """A basic state machine model
    """

    def __init__(self, master):
        self.currentState = StateMachine.empty_state
        self.currentState.update(master)
    
    def run(self, master):
        self.currentState = self.currentState.update(master)
        self.currentState.run(master)


StateMachine.pregame_state = PregameState()
StateMachine.empty_state = EmptyState()
StateMachine.game_state = GameState()


class MasterState:
    """The master state class that holds all major bot related globals"""

    def __init__(self):
        self._boottime = time.time()
        self._pregame = Pregame()
        self._game = None
        self._session = BotState.empty
        self._game_packs = dict()

        self.state_machine = StateMachine(self)
        self.state_machine.run(self)
    
    @property
    def boottime(self):
        return self._boottime

    @property
    def pregame(self):
        return self._pregame
    
    @pregame.setter
    def pregame(self, new):
        self._pregame = new
    
    @property
    def game(self):
        return self._game
    
    @game.setter
    def game(self, new):
        self._game = new
    
    @property
    def session(self):
        return self._session
    
    @property
    def game_packs(self):
        return self._game_packs
    
    def add_pack(self, pack):
        self._game_packs.update(pack)
    
    def sync_state(self):
        if self.session == BotState.pregame:
            self.transition_to_pregame()
        elif self.session == BotState.empty:
            self.transition_to_empty()
        else:
            assert self.session == BotState.game, "Inappropriate bot state"
            self.transition_to_game()
    
    def transition_to_pregame(self):
        self._session = BotState.pregame
        self.game = None
    
    def transition_to_empty(self):
        self._session = BotState.empty
        self.pregame.clear()
        self.game = None
    
    def transition_to_game(self):
        import botutils
        if botutils.lobby_timeout.is_running():
            botutils.lobby_timeout.cancel()
        self._session = BotState.game
        self.pregame.clear()
    
    def __str__(self):
        return f"Master State at pregame: {str(self.pregame)}, and game:{str(self.game)}"

    def __repr__(self):
        return self.__str__()

