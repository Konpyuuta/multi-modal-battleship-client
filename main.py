'''
Multi-Modal Battleship Game Client
-----------------------------------
This is the main entry point for the battleship game client application.

@author Maurice Amon
@version 1.0
@date March 2025
'''

# ===== IMPORTS =====
# standard library imports
import sys
import threading

# QT Framework imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Speech command import
# from commands.speech.StartSpeechModuleCommand import StartSpeechModuleCommand

# Application command import
from commands.StartGameCommand import StartGameCommand
from commands.requests.StartGameRequest import StartGameRequest
from model.socket.SocketConnection import SocketConnection

# Application view imports
from view.SocketConfigurationWindow import SocketConfigurationWindow
from view.StartWindow import StartWindow

# ===== APPLICATION INITIALIZATION =====

#command = StartSpeechModuleCommand()
#command.execute()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.


app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = StartWindow()
window.init_components()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Start the event loop.
app.exec()
