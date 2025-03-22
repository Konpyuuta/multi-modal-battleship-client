'''

@author Maurice Amon
'''

class MoveRequest:

    _playerID = None

    _col = None

    _row = None

    _is_valid = None

    def __init__(self, playerID, col, row):
        self._playerID = playerID
        self._col = col
        self._row = row

    def set_is_valid(self, is_valid):
        self._is_valid = is_valid

    def is_valid(self):
        return self._is_valid

    def getPlayerID(self):
        return self._playerID

    def getCol(self):
        return self._col

    def getRow(self):
        return self._row

