'''

@author Maurice Amon
'''
import time

from commands.StartGameCommand import StartGameCommand
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.requests.StartGameRequest import StartGameRequest
from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData
from view.GameWindow import GameWindow
import threading

class StartNewGameController:

    _start_game_command = None

    def __init__(self):
        self._start_game_command = StartGameCommand()


    def continously_fetch_game_data(self):
        is_game_over = False
        while is_game_over != 1:
            time.sleep((2))
            fetch_request = FetchGameStateRequest(SocketData().get_name(), "Fetch")
            s = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
            s.connect()
            game_state = s.send_request(fetch_request)
            is_game_over = game_state.get_game_state()
            self._game_window.update_player_grid(game_state.get_player_matrix())
            self._game_window.update_opponent_grid(game_state.get_opponent_matrix())


    def start_new_game_controller(self, start_window):
        start_window.hide()

        # Print detailed connection info
        print(f"Game server IP: {SocketData().get_ip_address()}")
        print(f"Game server port: {SocketData().get_port()}")

        # Create and send the start request
        print('Sending start game request...')
        start_request = StartGameRequest(SocketData().get_name(), "START THE GAME !!")
        socket = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
        socket.connect()
        game_state = socket.send_request(start_request)

        print("Received game state response:")
        print(game_state)

        # Initialize the game window
        print("Creating game window...")
        self._game_window = GameWindow()

        # Show the window first
        print("Showing game window...")
        self._game_window.show()

        # Empty opponent grid - since we don't know their ships yet
        empty_opponent_grid = [[0 for _ in range(10)] for _ in range(10)]

        # Update the grids
        print("Updating grids...")
        self._game_window.update_player_grid(game_state.get_player_matrix().get_matrix())
        self._game_window.update_opponent_grid(empty_opponent_grid)

        # Start the update thread after window is shown
        print("Starting update thread...")
        self._game_window.start_thread()

        print("Game initialization complete")


    def show_game_window(self):
        self._game_window.show()



