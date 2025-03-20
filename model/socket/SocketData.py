'''

@author Maurice Amon
'''

class SocketData(object):

    _ip_address = None

    _port = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SocketData, cls).__new__(cls)
        return cls.instance

    def __init__(self, ip_address: str, port: int):
        self._ip_address = ip_address
        self._port = port


    def get_ip_address(self):
        return self._ip_address

    def get_port(self):
        return self._port