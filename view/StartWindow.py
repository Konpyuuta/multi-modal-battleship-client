'''

@author Maurice Amon
'''
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ProjectConstants import ProjectConstants
from commands.requests.StartGameRequest import StartGameRequest


class StartWindow(QMainWindow):

    def __init__(self, start_game_command):
        super().__init__()

        # store the game command
        self._start_game_command = start_game_command

        centered_widget = QWidget(self)
        # Set the central widget of the Window.
        self.setCentralWidget(centered_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # initialize the widgets title ..
        self.setWindowTitle(ProjectConstants.START_WINDOW_TITLE)
        self.setFixedSize(QSize(600, 250))

        # create game start button
        game_button = self.create_button(ProjectConstants.START_WINDOW_GAME_BUTTON)
        # Connect the button's clicked signal to the start_game method
        game_button.clicked.connect(self.on_start_game_clicked)

        #add buttons to layout
        # button = QPushButton("Press Me!")
        # button.setFixedSize(QSize(400, 100))
        layout.addWidget(game_button)
        layout.addWidget(self.create_button(ProjectConstants.START_WINDOW_CONFIG_BUTTON))

        centered_widget.setLayout(layout)

    def create_button(self, label: str):
        button = QPushButton(label)
        button.setFixedSize(QSize(400, 100))
        button.setStyleSheet(ProjectConstants.START_WINDOW_BUTTON_STYLE)
        return button

    def on_start_game_clicked(self):
        # Create a new StartGameRequest object with the playerID and a message
        request = StartGameRequest(1, "Hello World")

        # execute the start game command:
        self._start_game_command.execute(request)

