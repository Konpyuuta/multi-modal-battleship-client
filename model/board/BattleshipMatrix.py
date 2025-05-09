'''

@author Maurice Amon
'''
from random import randrange
import os

class BattleshipMatrix():

    # The values of the matrix can be 3 different values ..
    # 0: No ship, no bomb landed.
    # -1: No ship, a bomb landed. 1: A ship is there. 2: A ship is there and a bomb landed on it.
    _matrix = None
    # All different sizes of battleships ..
    _battleship_sizes = [5, 5, 4, 3, 3, 2, 2]

    def __init__(self):
        rows, columns = (10, 10)
        self._matrix = [[0 for i in range(columns)] for j in range(rows)]


    def get_matrix(self):
        return self._matrix

    def set_matrix(self, matrix):
        self._matrix = matrix


    def has_bomb_been_placed(self, column, row):
        if self._matrix[column][row] == -1 or self._matrix[column][row] == 2:
            return True
        return False

    def set_bomb_in_matrix(self, column, row):
        if self._matrix[column][row] == 0:
            self._matrix[column][row] = -1
            return False
        elif self._matrix[column][row] == 1:
            self._matrix[column][row] = 2
            return True


    def create_battleships(self):
        for i in self._battleship_sizes:
            positionX = randrange(10)
            positionY = randrange(10)
            coords = self.place_battleships(positionX, positionY, i)
            self.insert_battleships(coords)


    def place_battleships(self, column, row, size):
        coordinates = []
        if column+size < 10:
            for i in range(size):
                coordinates.append((column+i, row))
        elif row+size < 10:
            for i in range(size):
                coordinates.append((column, row+i))
        elif column-size < 10:
            for i in range(size):
                coordinates.append((column-i, row))
        elif row-size < 10:
            for i in range(size):
                coordinates.append((column, row-i))
        else:
            self.place_battleships(randrange(10), randrange(10), size)

        return coordinates

    def insert_battleships(self, coords):
        for i, j in coords:
            self._matrix[j][i] = 1


    def print_matrix(self):
        st = ""
        for i in range(10):
            s = ""
            for j in range(10):
                s += f'''| {self._matrix[i][j]} '''

            st += f'''{s}{os.linesep}'''

        print(st, sep=f'''{os.linesep}''')