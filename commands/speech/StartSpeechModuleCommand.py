'''

@author Maurice Amon
'''
import pyttsx3
import speech_recognition

from commands.Command import Command


class StartSpeechModuleCommand(Command):

    _recognizer = None

    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()

    def execute(self):
        while(1):
            try:
                with speech_recognition.Microphone() as datasource:
                    self._recognizer.adjust_for_ambient_noise(datasource, duration=0.2)
                    audio = self._recognizer.listen(datasource)
                    text = self._recognizer.recognize_google(audio)
                    text = text.lower()
                    print("The user said: " + text)
                    self.speech_to_text(text)
            except speech_recognition.RequestError as exception:
                print(exception)
            except speech_recognition.UnknownValueError as exception:
                print(exception)


    def speech_to_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()