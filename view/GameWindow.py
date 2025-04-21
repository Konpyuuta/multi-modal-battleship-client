'''
@author Your Name
@description Main game window that displays the battleship grid
'''
import sys
import time

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal

from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from model.socket.SocketConnection import SocketConnection
from view.BattleshipGrid import BattleshipGrid
from ProjectConstants import ProjectConstants

class GameUpdater(QThread):
    matrices = pyqtSignal(object, object)

    def run(self):
        is_game_over = 0
        while is_game_over != 1:
            time.sleep((2))
            fetch_request = FetchGameStateRequest("Kuroro", "Fetch")
            s = SocketConnection("127.0.0.1", 8080)
            s.connect()
            game_state = s.send_request(fetch_request)
            is_game_over = game_state.get_game_state()
            player_matrix = game_state.get_player_matrix().get_matrix()
            opponent_matrix = game_state.get_opponent_matrix().get_matrix()
            # Emit matrices to the GUI ...
            self.matrices.emit(player_matrix, opponent_matrix)



class GameWindow(QMainWindow):
    """
    Main window for the Battleship game that displays the grids and game controls.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ProjectConstants.PROJECT_NAME)
        self.resize(1200, 600)  # Adjust size as needed

        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Create player grid section
        player_section = QWidget()
        player_layout = QVBoxLayout(player_section)

        player_label = QLabel(ProjectConstants.GAME_WINDOW_PLAYER_LABEL)
        player_label.setAlignment(Qt.AlignCenter)
        player_label.setStyleSheet(ProjectConstants.GAME_WINDOW_LABELS_STYLE)

        # Initial empty grid for player
        self.player_grid = BattleshipGrid()

        player_layout.addWidget(player_label)
        player_layout.addWidget(self.player_grid)

        # Create opponent grid section
        opponent_section = QWidget()
        opponent_layout = QVBoxLayout(opponent_section)

        opponent_label = QLabel(ProjectConstants.GAME_WINDOW_OPPONENT_LABEL)
        opponent_label.setAlignment(Qt.AlignCenter)
        opponent_label.setStyleSheet(ProjectConstants.GAME_WINDOW_LABELS_STYLE)

        # Initial empty grid for opponent
        self.opponent_grid = BattleshipGrid()

        opponent_layout.addWidget(opponent_label)
        opponent_layout.addWidget(self.opponent_grid)

        # Add both sections to main layout
        main_layout.addWidget(player_section)
        main_layout.addWidget(opponent_section)

        self.setCentralWidget(main_widget)


    def start_thread(self):
        self.updater = GameUpdater()
        self.updater.matrices.connect(self.update_grids)
        self.updater.start()

    def update_grids(self, player_matrix, opponent_matrix):
        self.player_grid.update_grid(player_matrix)
        self.opponent_grid.update_grid(opponent_matrix)


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