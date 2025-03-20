'''

@author Maurice Amon
'''

# importing required libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

import threading

from commands.speech.StartSpeechModuleCommand import StartSpeechModuleCommand

#command = StartSpeechModuleCommand()
#command.execute()



from view.SocketConfigurationWindow import SocketConfigurationWindow
from view.StartWindow import StartWindow

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = StartWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
