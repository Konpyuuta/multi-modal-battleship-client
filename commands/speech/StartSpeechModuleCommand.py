'''

@author Maurice Amon
'''
import itertools
import time

import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import QObject

from commands.Command import Command
from commands.requests.MoveRequest import MoveRequest
from commands.requests.RequestTypes import RequestTypes
from hand_recognition.HandRecognition import HandRecognition
from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData


class StartSpeechModuleCommand(QObject):

    _recognizer = None

    _microphone = None

    _x_coordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    _y_coordinates = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    _coord_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}

    _coordinates = None

    _stop_func = None

    def __init__(self):
        super().__init__()
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        product = list(itertools.product(self._x_coordinates, self._y_coordinates))
        concatenated = [a + b for a, b in product]
        self._coordinates = concatenated


    def start(self):
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)
        self._stop_func = self._recognizer.listen_in_background(self._microphone, self.callback)


    def stop(self):
        if self._stop_func:
            self._stop_func()
            self._stop_func = None

    def callback(self, recognizer, audio):
        try:
            text = recognizer.recognize_google(audio).lower()
            print("The user said: ", text)
            self.recognized.emit(text)
            if text in self._coordinates:
                self.init_move_request(1, 5)
            self.speech_to_text(text)
        except sr.UnknownValueError:
            print("error")
        except sr.RequestError:
            print("error")


    def speech_to_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def execute(self):
        while True:
            try:
                with sr.Microphone() as datasource:
                    self._recognizer.adjust_for_ambient_noise(datasource, duration=0.2)
                    audio = self._recognizer.listen_in_background(datasource)
                    text = self._recognizer.recognize_google(audio)
                    text = text.lower()
                    print("The user said: " + text)
                    if text in self._coordinates:
                        self.init_move_request(1, 5)
                        '''hr = HandRecognition()
                        gesture = hr.capture()
                        if gesture == 'pinching':
                            letter = text[0]
                            number = self._coord_dict[letter]
                            self.init_move_request(number, text[1])
                        elif gesture == 'Hand':
                            pass'''

                    self.speech_to_text(text)
            except sr.RequestError as exception:
                print(exception)
            except sr.UnknownValueError as exception:
                print(exception)

    def speech_to_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def init_move_request(self, col, row):
        print(f'speech event: Row: {row} Column: {col}')
        '''move_request = MoveRequest(RequestTypes.MOVE_REQUEST, SocketData().get_name(), row, col)
        s = SocketConnection(SocketData().get_ip_address(), int(SocketData().get_port()))
        s.connect()
        s.send_request(move_request)'''
