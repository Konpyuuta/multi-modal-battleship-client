'''

@author Maurice Amon
'''
from model.socket.SocketSingleton import SocketSingleton


class SocketData(metaclass=SocketSingleton):

    _name = None

    _ip_address = None

    _port = None

    _initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SocketData, cls).__new__(cls)
        return cls.instance

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_ip_address(self, ip_address):
        self._ip_address = ip_address

    def set_port(self, port):
        self._port = port

    def get_ip_address(self):
        return self._ip_address

    def get_port(self):
        return self._port