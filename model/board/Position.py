'''

@author Maurice Amon
'''

class Position:

    _square_position_list = None

    _bombed_squares_list = None

    _is_sunk = False

    def __init__(self, squares):
        self._square_position_list = squares


    def set_squares(self, squares):
        self._square_position_list = squares

    def set_bombed_squares(self, bombed_squares):
        self._bombed_squares_list = bombed_squares

    def add_bombed_square(self, bombed_square):
        self._bombed_squares_list.append(bombed_square)

    def set_is_sunk(self, is_sunk):
        self._is_sunk = is_sunk

    def get_squares(self):
        return self._square_position_list

    def get_bombed_squares(self):
        return self._bombed_squares_list

    def get_is_sunk(self):
        return self._is_sunk