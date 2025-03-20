'''

@author Maurice Amon
'''
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ProjectConstants import ProjectConstants


class StartWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        centered_widget = QWidget(self)
        # Set the central widget of the Window.
        self.setCentralWidget(centered_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        # initialize the widgets title ..
        self.setWindowTitle(ProjectConstants.START_WINDOW_TITLE)
        self.setFixedSize(QSize(600, 250))
        button = QPushButton("Press Me!")
        button.setFixedSize(QSize(400, 100))
        layout.addWidget(self.create_button(ProjectConstants.START_WINDOW_GAME_BUTTON))
        layout.addWidget(self.create_button(ProjectConstants.START_WINDOW_CONFIG_BUTTON))
        centered_widget.setLayout(layout)


    def create_button(self, label: str):
        button = QPushButton(label)
        button.setFixedSize(QSize(400, 100))
        button.setStyleSheet(ProjectConstants.START_WINDOW_BUTTON_STYLE)
        return button
