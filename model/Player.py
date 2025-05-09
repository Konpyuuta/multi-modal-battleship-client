'''

@author Maurice Amon

Represents a player
'''

class Player:

    _name = None

    _is_turn = None

    _battleships = None

    _heart_rate = None

    def __init__(self):
        pass

    def set_name(self, name):
        self._name = name

    def set_is_turn(self, is_turn):
        self._is_turn = is_turn

    def set_battleships(self, battleships):
        self._battleships = battleships


    def set_heart_rate(self, heart_rate):
        self._heart_rate = heart_rate

    def get_name(self):
        return self._name

    def get_is_turn(self):
        return self._is_turn

    def get_battleships(self):
        return self._battleships


    def get_heart_rate(self):
        return self._heart_rate