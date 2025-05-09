'''

@author Maurice Amon
'''
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ProjectConstants import ProjectConstants
from controller.EditConfigurationsController import EditConfigurationsController
from controller.StartNewGameController import StartNewGameController
from view.SocketConfigurationWindow import SocketConfigurationWindow


class StartWindow(QMainWindow):

    _start_new_game_controller = None
    _edit_config_controller = None
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = QMainWindow.__new__(class_, *args, **kwargs)
        return class_._instance

    def init_components(self):

        # store the game command
        self._start_new_game_controller = StartNewGameController()
        self._edit_config_controller = EditConfigurationsController()
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
        edit_button = self.create_button(ProjectConstants.START_WINDOW_CONFIG_BUTTON)
        # Connect the button's clicked signal to the start_game method
        game_button.clicked.connect(lambda: self._start_new_game_controller.start_new_game_controller(self))
        edit_button.clicked.connect(self.show_edit_configurations)

        #add buttons to layout
        # button = QPushButton("Press Me!")
        # button.setFixedSize(QSize(400, 100))
        layout.addWidget(game_button)
        layout.addWidget(edit_button)

        centered_widget.setLayout(layout)


    def create_button(self, label: str):
        button = QPushButton(label)
        button.setFixedSize(QSize(400, 100))
        button.setStyleSheet(ProjectConstants.START_WINDOW_BUTTON_STYLE)
        return button

    def on_start_game_clicked(self):
        pass
        #socket = SocketConnection("127.0.0.1", 8080)
        #socket.connect()
        #matrix = socket.send_request(start_request)


    def show_edit_configurations(self):
        self._socket_window = SocketConfigurationWindow()
        self._socket_window.show()
