'''

@author Maurice Amon
'''

import socket

import sys

class SocketConnection:

    _ip = None

    _port = None

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port


    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
        s.connect(self._ip, self._port)
        print("Socket connected")



