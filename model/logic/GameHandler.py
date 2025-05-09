'''

@author Maurice Amon

@description In charge of implementing the game logic of our Enhanced Battleship.
             Uses a deterministic finite Automaton (DFA) to implement the rules.
             Takes an input from the socket-stream to trigger the rule-enforcement.
'''
from model.logic.states.GameOverState import GameOverState
from model.logic.states.StartGameState import StartGameState
from model.logic.states.TurnState import TurnState


class GameHandler:

    _start_state = None

    _turn_state = None

    _game_over_state = None

    _current_state = None

    def __init__(self, game):
        self._start_state = StartGameState(game)
        self._turn_state = TurnState(game)
        self._game_over_state = GameOverState(game)
        self._current_state = self._start_state


    def handle(self):
        pass

    def set_current_state(self, state):
        self._current_state = state


    def get_current_state(self):
        return self._current_state
