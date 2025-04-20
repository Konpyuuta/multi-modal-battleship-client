'''
@author Alessia
@description Command to handle starting a new game
'''
from commands.requests.StartGameRequest import StartGameRequest
from model.board.BattleshipMatrix import BattleshipMatrix
from view.GameWindow import GameWindow


class StartGameCommand:
    """
    Command to handle the StartGameRequest and initialize the game.
    """

    def __init__(self):
        """
        Initialize the StartGameCommand.
        """
        self._game_window = None
        self._start_window = None

    def set_start_window(self, window):
        """
        Set the reference to the start window that will be hidden when the game starts.

        Args:
            window: The start window instance
        """
        self._start_window = window

    def execute(self, request):
        """
        Execute the start game command.

        Args:
            request: The StartGameRequest containing player information
        """
        #print(f"Starting game for player {request.get_playerID()} with message: {request.get_message()}")

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
        self._game_window.update_player_grid(example_player_grid)
        self._game_window.update_opponent_grid(empty_opponent_grid)

        # Hide the start window if it's set
        if self._start_window:
            self._start_window.hide()

        # Show the game window
        self._game_window.show()

        # Send a request to the server to initialize the game
        #self._send_to_server(request)

    def _send_to_server(self, request):
        """
        Send the start game request to the server.
        This would be implemented based on your client-server communication protocol.
        """
        pass
