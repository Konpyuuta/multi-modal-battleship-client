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


    def connect(self):
        print("Socket created")
        self._s.connect((self._ip, self._port))
        print("Socket connected")

    def send_request(self, request):
        self._s.send(pickle.dumps(request))
        data = ''
        data = self._s.recv(1024).decode()
        print(data)



