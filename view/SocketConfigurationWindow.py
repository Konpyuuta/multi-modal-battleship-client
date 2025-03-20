'''

@author Maurice Amon
'''
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

from ProjectConstants import ProjectConstants


class SocketConfigurationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ProjectConstants.SOCKET_CONFIG_WINDOW_TITLE)
        self.setGeometry(100, 100, 700, 300)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create the labels ..
        ip_label = QLabel(ProjectConstants.SOCKET_CONFIG_WINDOW_IP)
        port_label = QLabel(ProjectConstants.SOCKET_CONFIG_WINDOW_PORT)
        self.add_label_style(ip_label)
        self.add_label_style(port_label)
        # Create the input boxes ..
        ip_field = self.create_input_field("Type IP address ...")
        port_field = self.create_input_field("Type port number ...")
        layout.addWidget(ip_label)
        layout.addWidget(ip_field)
        layout.addWidget(port_label)
        layout.addWidget(port_field)
        layout.addWidget(self.create_button("Confirm"))

        central_widget.setLayout(layout)


    def create_button(self, label: str):
        button = QPushButton(label)
        button.setFixedSize(QSize(100, 40))
        button.setStyleSheet(ProjectConstants.START_WINDOW_BUTTON_STYLE)
        return button


    def add_label_style(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Arial', 14))

    def create_input_field(self, placeholder: str):
        input_box = QLineEdit()
        input_box.setPlaceholderText(placeholder)
        input_box.setFixedHeight(60)
        input_box.setFont(QFont('Arial', 12))
        return input_box

