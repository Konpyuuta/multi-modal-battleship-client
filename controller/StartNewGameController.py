'''

@author Maurice Amon
'''
from commands.StartGameCommand import StartGameCommand
from commands.requests.StartGameRequest import StartGameRequest
from model.socket.SocketConnection import SocketConnection
from view.GameWindow import GameWindow


class StartNewGameController:

    _start_game_command = None

    def __init__(self):
        self._start_game_command = StartGameCommand()


    def start_new_game_controller(self, start_window):
        start_window.hide()
        start_request = StartGameRequest("Kuroro", "START THE GAME !!")
        socket = SocketConnection("127.0.0.1", 8080)
        socket.connect()
        print("Hiiiii")
        matrix = socket.send_request(start_request)
        print("Hiiiii")
        print(matrix)
        # Initialize the game window
        self._game_window = GameWindow()

        # Example grid initialization - this would come from the server
        # For testing purposes I've created a sample grid
        example_player_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, -1, -1, -1, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        #print(matrix.print_matrix())
        #example_player_grid = matrix.get_matrix()

        # Empty opponent grid - since we don't know their ships yet
        empty_opponent_grid = [[0 for _ in range(10)] for _ in range(10)]

        # Update the grids
        self._game_window.update_player_grid(matrix.get_matrix())
        self._game_window.update_opponent_grid(empty_opponent_grid)
        # Show the game window
        self._game_window.show()

