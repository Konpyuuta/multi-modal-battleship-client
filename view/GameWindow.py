'''
@author Alessia Bussard
@description Main game window that displays the battleship grid
'''
import sys
import time

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal

from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData
from view.BattleshipGrid import BattleshipGrid
from ProjectConstants import ProjectConstants
from view.HeartRateDisplay import HeartRateDisplay
from commands.heart_rate.EmotiBitClient import EmotiBitClient

class GameUpdater(QThread):
    matrices = pyqtSignal(object, object, object, object)

    def run(self):
        is_game_over = 0
        winner = None
        while is_game_over != 1:
            time.sleep((2))
            fetch_request = FetchGameStateRequest(SocketData().get_name(), "Fetch")
            s = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
            s.connect()
            game_state = s.send_request(fetch_request)
            is_game_over = game_state.get_game_state()
            if is_game_over == 1:
                winner = game_state.get_winner()
            is_turn = game_state.is_turn()
            print(f"Player matrix: {game_state.get_player_matrix().get_matrix()}")
            print(f"Player2 matrix: {game_state.get_opponent_matrix().get_matrix()}")
            player_matrix = game_state.get_player_matrix().get_matrix()
            opponent_matrix = game_state.get_opponent_matrix().get_matrix()
            # Emit matrices to the GUI ...
            self.matrices.emit(player_matrix, opponent_matrix, is_turn, winner)



class GameWindow(QMainWindow):
    """
    Main window for the Battleship game that displays the grids and game controls.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ProjectConstants.PROJECT_NAME)
        self.resize(1200, 700)  # Adjust size as needed

        # Initialize EmotiBit client
        self.emotibit = EmotiBitClient.get_instance()
        self.emotibit.heart_rate_updated.connect(self.update_player_heart_rate)
        # For opponent heart rate (this signal would need to be added to EmotiBitClient)
        if hasattr(self.emotibit, 'opponent_heart_rate_updated'):
            self.emotibit.opponent_heart_rate_updated.connect(self.update_opponent_heart_rate)

        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Create grids layout
        grids_layout = QHBoxLayout()

        # Create player grid section
        player_section = QWidget()
        player_layout = QVBoxLayout(player_section)

        player_label = QLabel(ProjectConstants.GAME_WINDOW_PLAYER_LABEL)
        player_label.setAlignment(Qt.AlignCenter)
        player_label.setStyleSheet(ProjectConstants.GAME_WINDOW_LABELS_STYLE)

        # Initial empty grid for player
        self.player_grid = BattleshipGrid(False)

        player_layout.addWidget(player_label)
        player_layout.addWidget(self.player_grid)

        # Create opponent grid section
        opponent_section = QWidget()
        opponent_layout = QVBoxLayout(opponent_section)

        opponent_label = QLabel(ProjectConstants.GAME_WINDOW_OPPONENT_LABEL)
        opponent_label.setAlignment(Qt.AlignCenter)
        opponent_label.setStyleSheet(ProjectConstants.GAME_WINDOW_LABELS_STYLE)

        # Initial empty grid for opponent
        self.opponent_grid = BattleshipGrid(True)

        opponent_layout.addWidget(opponent_label)
        opponent_layout.addWidget(self.opponent_grid)

        # Add both sections to main layout
        grids_layout.addWidget(player_section)
        grids_layout.addWidget(opponent_section)

        # Create heart rate display layout
        hr_layout = QHBoxLayout()
        self.opponent_hr_display = HeartRateDisplay("Opponent")
        hr_layout.addWidget(self.opponent_hr_display)

        # Add layouts to main layout
        main_layout.addLayout(grids_layout)
        main_layout.addLayout(hr_layout)

        self.setCentralWidget(main_widget)


    def show_winner_dialog(self, player_name):
        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over")
        msg.setText(f"🏆 {player_name} has won the game!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        if msg.exec_() == QMessageBox.Ok:
            QApplication.quit()

    def start_thread(self):
        self.updater = GameUpdater()
        self.updater.matrices.connect(self.update_grids)
        self.updater.start()

    def update_grids(self, player_matrix, opponent_matrix, is_turn, winner):
        self.player_grid.update_grid(player_matrix)
        self.opponent_grid.update_grid(opponent_matrix)
        if not is_turn:
            self.opponent_grid.disable_cells()
        else:
            self.opponent_grid.enable_cells()
        print(f"IS_TURN: {is_turn}")
        if winner is not None:
            self.show_winner_dialog(winner)


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

    def update_player_heart_rate(self, heart_rate):
        """
        Update the player's heart rate display
        """
        self.player_hr_display.update_heart_rate(heart_rate)

    def update_opponent_heart_rate(self, player_id, heart_rate):
        """
        Update the opponent's heart rate display
        """
        self.opponent_hr_display.update_heart_rate(heart_rate)