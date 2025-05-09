'''

@author Maurice Amon
'''
import random
import string

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QApplication

from ProjectConstants import ProjectConstants
from controller.SaveConfigurationController import SaveConfigurationController
from model.socket.SocketData import SocketData


class SocketConfigurationWindow(QMainWindow):

    _edit_controller = None

    _input_field = None

    _ip_field = None

    _port_field = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ProjectConstants.SOCKET_CONFIG_WINDOW_TITLE)
        self.setGeometry(100, 100, 700, 300)
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().screenGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

        self._edit_controller = SaveConfigurationController()
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create the labels ..
        name_label = QLabel("Username ..")
        ip_label = QLabel(ProjectConstants.SOCKET_CONFIG_WINDOW_IP)
        port_label = QLabel(ProjectConstants.SOCKET_CONFIG_WINDOW_PORT)
        self.add_label_style(name_label)
        self.add_label_style(ip_label)
        self.add_label_style(port_label)
        # Create the input boxes ..
        self._name_field = self.create_input_field("Type username ...")
        self._name_field.setText(''.join(random.choice(string.ascii_letters) for _ in range(10)))
        self._ip_field = self.create_input_field("Type IP address ...")
        self._ip_field.setText("127.0.0.1")
        self._port_field = self.create_input_field("Type port number ...")
        self._port_field.setText("8080")
        layout.addWidget(name_label)
        layout.addWidget(self._name_field)
        layout.addWidget(ip_label)
        layout.addWidget(self._ip_field)
        layout.addWidget(port_label)
        layout.addWidget(self._port_field)

        # Confirm button ..
        confirm_button = self.create_button("Confirm")
        confirm_button.clicked.connect(self.save_configurations)
        layout.addWidget(confirm_button)

        central_widget.setLayout(layout)


    def save_configurations(self):
        sd = SocketData()
        sd.set_name(self._name_field.text())
        sd.set_ip_address(self._ip_field.text())
        sd.set_port(self._port_field.text())
        self.close()


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
