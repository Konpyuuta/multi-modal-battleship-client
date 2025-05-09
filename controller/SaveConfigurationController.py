'''

@author Maurice Amon
'''
from model.socket.SocketData import SocketData


class SaveConfigurationController:

    _edit = False

    _socket_window = None

    def __init__(self):
        self._edit = True


    def save_configurations(self, sw, name, ip, port):
        self._socket_window = sw
        self._socket_window.close()
        sd = SocketData(name, ip, port)

