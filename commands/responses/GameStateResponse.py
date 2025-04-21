'''

@author Maurice Amon
'''
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.responses.Response import Response


class GameStateResponse(Response):

    _player_matrix = None

    _opponent_matrix = None

    _player_matrix = None

    _is_turn = None

    # 0: Running game, 1: Game Over
    _game_state = None

    def __init__(self, player_matrix, opponent_matrix, game_state, fetchGameRequest: FetchGameStateRequest):
        self._player_matrix = player_matrix
        self._opponent_matrix = opponent_matrix
        self._game_state = game_state
        self._fetchGameRequest = fetchGameRequest

    def get_player_matrix(self):
        return self._player_matrix

    def get_opponent_matrix(self):
        return self._opponent_matrix

    def get_game_state(self):
        return self._game_state
