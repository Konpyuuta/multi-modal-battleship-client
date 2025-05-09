'''

@author Maurice Amon
'''
from view.SocketConfigurationWindow import SocketConfigurationWindow


class EditConfigurationsController:

    _edit = False

    _socket_window = None

    _start_window = None

    def __init__(self):
        self._edit = True

    def show_edit_configurations(self, sw):
        self._socket_window = SocketConfigurationWindow()
        self._socket_window.show()


