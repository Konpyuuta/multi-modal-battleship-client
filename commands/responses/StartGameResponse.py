'''

@author Maurice Amon
'''
from commands.responses.Response import Response


class StartGameResponse(Response):

    _message = None

    _is_turn = None

    def __init__(self, is_turn):
        self._message = "START-GAME"
        self._is_turn = is_turn


    def get_message(self):
        return self._message

    def is_turn(self):
        return self._is_turn