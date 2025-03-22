'''

@author Maurice Amon
@description Requests a new game ..
'''

class StartGameRequest:

    _playerID = None

    _message = None

    def __init__(self, playerID, message: str):
        self._playerID = playerID
        self._message = message


    def get_message(self):
        return self._message

    def get_playerID(self):
        return self._playerID