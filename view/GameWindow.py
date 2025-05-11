'''
@author Your Name
@description Main game window that displays the battleship grid
'''
import sys
import threading
import time

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QApplication, QFrame
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal

from SpeechAndGestureThread import SpeechAndGestureThread
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.requests.MoveRequest import MoveRequest
from commands.requests.RequestTypes import RequestTypes
from commands.speech.StartSpeechModuleCommand import StartSpeechModuleCommand
from heart_rate.EmotiBitClient import EmotiBitClient
from heart_rate.HeartRate import HeartRate
from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData
from view.BattleshipGrid import BattleshipGrid
from ProjectConstants import ProjectConstants

class GameUpdater(QThread):
    matrices = pyqtSignal(object, object, object, object, object)

    def run(self):
        is_game_over = 0
        winner = None

        emoti_client = EmotiBitClient()
        emoti_client.start()
        while is_game_over != 1:
            time.sleep((2))
            fetch_request = FetchGameStateRequest(SocketData().get_name(), "Fetch")
            fetch_request.set_heart_rate(HeartRate().get_heart_rate())
            s = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
            s.connect()
            game_state = s.send_request(fetch_request)
            is_game_over = game_state.get_game_state()
            if is_game_over == 1:
                winner = game_state.get_winner()
            is_turn = game_state.is_turn()
            player_matrix = game_state.get_player_matrix().get_matrix()
            opponent_matrix = game_state.get_opponent_matrix().get_matrix()
            # Emit matrices to the GUI ...
            self.matrices.emit(player_matrix, opponent_matrix, is_turn, winner, game_state.get_heart_rate())



class GameWindow(QMainWindow):
    """
    Main window for the Battleship game that displays the grids and game controls.
    """

    _colors = ["yellow", "orange", "red"]

    _is_turn = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ProjectConstants.PROJECT_NAME)
        self.resize(1200, 600)  # Adjust size as needed

        self.color_box = QFrame()
        self.color_box.setFixedSize(100, 100)
        self.color_box.setStyleSheet("background-color: gray; border solid black;")

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
        main_layout.addWidget(player_section)
        main_layout.addWidget(opponent_section)
        main_layout.addWidget(self.color_box)

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
        self.speech_thread = SpeechAndGestureThread("activate")
        self.speech_thread.command_confirmed.connect(self.on_command_confirmed)
        self.speech_thread.start()

    def on_command_confirmed(self, col, row, gesture):
        if self._is_turn:
            print("Execute Move ..")
            move_request = MoveRequest(RequestTypes.MOVE_REQUEST, SocketData().get_name(), row, col)
            s = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
            s.connect()
            s.send_request(move_request)

        # You can now run socket or any action based on this

    def closeEvent(self, event):
        self.speech_thread.stop()
        event.accept()


    def update_grids(self, player_matrix, opponent_matrix, is_turn, winner, heart_rate):
        self._is_turn = is_turn
        color = "gray"
        if heart_rate >= 60.0 and heart_rate <= 70.0:
            color = "yellow"
        elif heart_rate > 70.0 and heart_rate <= 80:
            color = "orange"
        elif heart_rate > 80:
            color = "red"
        self.color_box.setStyleSheet(f"background-color: {color}; border solid black;")

        self.player_grid.update_grid(player_matrix)
        self.opponent_grid.update_grid(opponent_matrix)
        if not is_turn:
            self.opponent_grid.disable_cells()
        else:
            self.opponent_grid.enable_cells()
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
