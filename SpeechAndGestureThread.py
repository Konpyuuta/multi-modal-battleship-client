'''

@author Maurice Amon
'''
import itertools

from PyQt5.QtCore import QThread, pyqtSignal

import speech_recognition as sr


class SpeechAndGestureThread(QThread):

    _x_coordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    _y_coordinates = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    _coord_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}

    _coordinates = None

    command_confirmed = pyqtSignal(int, int, str)  # command, gesture

    def __init__(self, target_word="activate"):
        super().__init__()
        product = list(itertools.product(self._x_coordinates, self._y_coordinates))
        concatenated = [a + b for a, b in product]
        self._coordinates = concatenated
        print(self._coordinates)
        self.target_word = target_word.lower()
        self.running = True
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self):
        while self.running:
            if self.fetch_coordinates():
                print("Coordinates detected. Waiting for gesture...")
                gesture = self.wait_for_gesture(timeout=5)
                print(f"Gesture: {gesture}")
                if gesture == "Pinching":
                    col = int(self._coord_dict[self._coord[0]])
                    row = int(self._coord[1:])-1
                    self.command_confirmed.emit(col, row, gesture)

    def fetch_coordinates(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=7)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized speech: {text}")
                if text in self._coordinates:
                    self._coord = text
                return text in self._coordinates
            except Exception:
                return False

    def wait_for_gesture(self, timeout=12):
        import cv2
        import mediapipe as mp
        import time

        mp_hands = mp.solutions.hands.Hands()
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        gesture_name = None

        while time.time() - start_time < timeout and self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            results = mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture_name = self.classify_gesture(hand_landmarks, frame)
                    if gesture_name is not None:
                        cap.release()
                        return gesture_name

        cap.release()
        return gesture_name

    def classify_gesture(self, hand_landmarks, frame):
        # get landmark positions
        landmarks = hand_landmarks.landmark

        # get tip of thumb and tip of index finger
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        wrist = landmarks[0]

        # convert to pixel coordinates
        h, w, _ = frame.shape
        thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
        index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
        middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)

        # Gesture Recognition
        if abs(thumb_x - index_x) > 30 and abs(thumb_y - index_y) > 30 and abs(middle_x - index_x) > 30 and abs(
                middle_y - index_y) > 30:  # Fingers touching
            gesture = "Open hand"
        elif thumb_y < index_y:  # Thumb up
            gesture = "Thumbs Up"
        elif abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30:  # Fingers touching
            gesture = "Pinching"
        else:
            gesture = "Unknown"

        return gesture

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
