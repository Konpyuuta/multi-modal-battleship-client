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

# HeartRate import
from commands.heart_rate.EmotiBitClient import EmotiBitClient


# ===== EMOTIBIT INITIALIZATION =====
def initialize_emotibit():
    """Initialize and start the EmotiBitClient"""
    print("Initializing EmotiBit client...")

    # Get the singleton instance
    emotibit = EmotiBitClient.get_instance()

    # Connect signal to log heart rate updates
    emotibit.heart_rate_updated.connect(on_heart_rate_updated)

    # Start the client (this starts the processing threads)
    emotibit.start()

    # Set up a timer to check if we're getting data
    timer = QTimer()
    timer.singleShot(10000, check_emotibit_data)

    print("EmotiBit client initialized")

    return emotibit


def on_heart_rate_updated(heart_rate):
    """Handle heart rate updates from EmotiBit"""
    print(f"Heart rate update: {heart_rate:.1f} BPM")
    # You can add UI updates or game effects here if needed


def check_emotibit_data():
    """Check if we're receiving data from EmotiBit"""
    emotibit = EmotiBitClient.get_instance()
    current_hr = emotibit.get_current_heart_rate()

    if current_hr > 0:
        print(f"EmotiBit check: Receiving heart rate data ({current_hr:.1f} BPM)")
    else:
        print("EmotiBit check: No heart rate data received. Check your EmotiBit connection.")
        # Schedule another check
        timer = QTimer()
        timer.singleShot(10000, check_emotibit_data)

# ===== APPLICATION INITIALIZATION =====

#command = StartSpeechModuleCommand()
#command.execute()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.


app = QApplication(sys.argv)

emotibit = initialize_emotibit()

# Create a Qt widget, which will be our window.
window = StartWindow()
window.init_components()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Exit the application as soon as the user closes the Window ..
sys.exit(app.exec_())
