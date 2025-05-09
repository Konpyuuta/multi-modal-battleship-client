'''

@author Maurice Amon
'''
from commands.requests.Request import Request
from commands.requests.RequestTypes import RequestTypes


class FetchGameStateRequest(Request):

    _playerID = None

    _message = None

    _heart_rate = None

    def __init__(self, playerID, message: str):
        super()
        self._playerID = playerID
        self._message = message
        self._request_type = RequestTypes.FETCH_REQUEST

    def set_heart_rate(self, heart_rate):
        self._heart_rate = heart_rate

    def get_heart_rate(self):
        return self._heart_rate

    def get_message(self):
        return self._message

    def get_playerID(self):
        return self._playerID

    def get_request_type(self):
        return self._request_type