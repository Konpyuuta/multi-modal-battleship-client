class StartGameCommand:
    def execute(self, request):
        #simple print statement to test the execution
        print(f"Game started for player: {request.get_playerID()}")
        print(f"Message: {request.get_message()}")

# class StartGameCommand:
#     def __init__(self, game_service):
#
#         self._game_service = game_service
#
#     def execute(self, request):
#         try:
#             # Extract player ID from the request
#             player_id = request.get_playerID()
#
#             # Use the game service to initialize the game
#             game = self._game_service.initialize_game(player_id)
#
#             # Additional game start logic
#             print(f"Game started for player: {player_id}")
#
#             return game
#
#         except Exception as e:
#             # Handle any errors during game initialization
#             print(f"Error starting game: {e}")
#             raise
