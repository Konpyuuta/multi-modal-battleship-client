'''

@author Maurice Amon
'''
from commands.responses.Response import Response


class MoveResponse(Response):

    _battle_ship_matrix = None

    _message = None

    def __init__(self, battle_ship_matrix, message):
        self._battle_ship_matrix = battle_ship_matrix
        self._message = message

    def get_battle_ship_matrix(self):
        return self._battle_ship_matrix

    def get_message(self):
        return self._message
