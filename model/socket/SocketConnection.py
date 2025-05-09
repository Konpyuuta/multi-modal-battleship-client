'''

@author Maurice Amon
'''
import json
import pickle
import socket

import sys

class SocketConnection:

    _ip = None

    _port = None

    _s = None

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.settimeout(None)


    def connect(self):
        self._s.connect((self._ip, self._port))

    def send_request(self, request):
        self._s.send(pickle.dumps(request))
        res = self._s.recv(2048)
        data = pickle.loads(res)
        return data



