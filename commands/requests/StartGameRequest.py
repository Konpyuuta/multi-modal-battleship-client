'''

@author Maurice Amon
@description Requests a new game ..
'''
from commands.requests.Request import Request
from commands.requests.RequestTypes import RequestTypes


class StartGameRequest(Request):

    _playerID = None

    _message = None

    def __init__(self, playerID, message: str):
        super()
        self._playerID = playerID
        self._message = message
        self._request_type = RequestTypes.START_REQUEST


    def get_message(self):
        return self._message

    def get_playerID(self):
        return self._playerID
