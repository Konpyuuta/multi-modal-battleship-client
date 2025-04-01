'''
@author Your Name
@description Main game window that displays the battleship grid
'''
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize

from view.BattleshipGrid import BattleshipGrid
from ProjectConstants import ProjectConstants


class GameWindow(QMainWindow):
    """
    Main window for the Battleship game that displays the grids and game controls.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Battleship Game")
        self.resize(1200, 600)  # Adjust size as needed

        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Create player grid section
        player_section = QWidget()
        player_layout = QVBoxLayout(player_section)

        player_label = QLabel("Your Ships")
        player_label.setAlignment(Qt.AlignCenter)
        player_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Initial empty grid for player
        self.player_grid = BattleshipGrid()

        player_layout.addWidget(player_label)
        player_layout.addWidget(self.player_grid)

        # Create opponent grid section
        opponent_section = QWidget()
        opponent_layout = QVBoxLayout(opponent_section)

        opponent_label = QLabel("Opponent's Waters")
        opponent_label.setAlignment(Qt.AlignCenter)
        opponent_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Initial empty grid for opponent
        self.opponent_grid = BattleshipGrid()

        opponent_layout.addWidget(opponent_label)
        opponent_layout.addWidget(self.opponent_grid)

        # Add both sections to main layout
        main_layout.addWidget(player_section)
        main_layout.addWidget(opponent_section)

        self.setCentralWidget(main_widget)

    def update_player_grid(self, grid_data):
        """
        Update the player's grid with new data.
        """
        self.player_grid.update_grid(grid_data)

    def update_opponent_grid(self, grid_data):
        """
        Update the opponent's grid with new data.
        """
        self.opponent_grid.update_grid(grid_data)