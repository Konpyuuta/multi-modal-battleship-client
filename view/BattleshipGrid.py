import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt, QRect, QRectF, QPointF, QSize
from view.BattleshipCell import BattleshipCell


class BattleshipGrid(QWidget):
    """
    Widget for the Battleship game grid.
    """

    def __init__(self, grid_data=None, parent=None):
        super().__init__(parent)
        self.grid_size = 10  # 10x10 grid

        # Initialize empty grid_data if none provided
        if grid_data is None:
            self.grid_data = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        else:
            self.grid_data = grid_data

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(1)  # Small spacing between cells

        # Create cells and headers
        self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Add column headers (A-J)
        for j in range(self.grid_size):
            header = QLabel(chr(65 + j))  # ASCII 'A' starts at 65
            header.setAlignment(Qt.AlignCenter)
            header.setStyleSheet("font-weight: bold;")
            layout.addWidget(header, 0, j + 1)

        # Add row headers (1-10)
        for i in range(self.grid_size):
            header = QLabel(str(i + 1))
            header.setAlignment(Qt.AlignCenter)
            header.setStyleSheet("font-weight: bold;")
            layout.addWidget(header, i + 1, 0)

        # Analyze the grid to determine ship connections
        ship_connections = self._get_ship_connections()

        # Add cells to the grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_state = self.grid_data[i][j]
                conn = ship_connections[i][j] if cell_state in [1, 2] else None

                cell = BattleshipCell(state=cell_state, ship_connections=conn)
                layout.addWidget(cell, i + 1, j + 1)
                self.cells[i][j] = cell

        self.setLayout(layout)

    def _get_ship_connections(self):
        """
        Analyze the grid to determine ship connections for each cell.
        Returns a 2D array of connection dictionaries for each cell.
        """
        connections = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid_data[i][j] in [1, 2]:  # If there's a ship
                    # Check for connections in all directions
                    conn = {
                        'top': False,
                        'right': False,
                        'bottom': False,
                        'left': False
                    }

                    # Check top
                    if i > 0 and self.grid_data[i - 1][j] in [1, 2]:
                        conn['top'] = True

                    # Check right
                    if j < self.grid_size - 1 and self.grid_data[i][j + 1] in [1, 2]:
                        conn['right'] = True

                    # Check bottom
                    if i < self.grid_size - 1 and self.grid_data[i + 1][j] in [1, 2]:
                        conn['bottom'] = True

                    # Check left
                    if j > 0 and self.grid_data[i][j - 1] in [1, 2]:
                        conn['left'] = True

                    connections[i][j] = conn

        return connections

    def update_grid(self, grid_data):
        """
        Update the grid with new data.
        """
        self.grid_data = grid_data
        ship_connections = self._get_ship_connections()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_state = self.grid_data[i][j]
                conn = ship_connections[i][j] if cell_state in [1, 2] else None

                # Update the cell
                self.cells[i][j].state = cell_state
                self.cells[i][j].ship_connections = conn
                self.cells[i][j].update()  # Trigger a repaint