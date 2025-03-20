'''

@author Maurice Amon
'''
from abc import ABC


class Board(ABC):

    _grid = None

    def __init__(self):
        rows, cols = (10, 10)
        self._grid = [[0]*cols]*rows

    def create_grid(self):
        pass