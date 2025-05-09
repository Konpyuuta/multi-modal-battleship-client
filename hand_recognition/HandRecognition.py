'''
@author Lucas Cornet

Hand detection algorithm with openCV and mediapipe
The camera record through webcam, recognize the movement and return the last hand gesture identified
'''

import cv2
import mediapipe as mp

class HandRecognition: 
    def __init__(self):
        """Initialize mediapipe hands"""
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands() #(min_detection_confidence=0.7, min_tracking_confidence=0.7)


    def bgr_to_rbg(self, frame):
        """convert bgr to rbg for mediapipe processing"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    def frame_process(self, rgb_frame):
        """process fram to detect hand"""
        return self.hands.process(rgb_frame)


    def hand_detection(self, result, frame):
        """detect hand landmarks and recognize gesture"""

        gesture = "Unknown"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # draw hand landmarks
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

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
                if abs(thumb_x - index_x) > 30 and abs(thumb_y - index_y) > 30 and abs(middle_x - index_x) > 30 and abs(middle_y - index_y) > 30  :  # Fingers touching
                    gesture = "Open hand"
                elif thumb_y < index_y:  # Thumb up
                    gesture = "Thumbs Up"
                elif abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30:  # Fingers touching
                    gesture = "Pinching"
                else:
                    gesture = "Unknown"

        return gesture


    def capture(self):
        # start capturing video
        cap = cv2.VideoCapture(0)  # 0 for default webcam

        last_gesture = 'Unknown'

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # convert BGR to RGB for mediapipe 
            rgb_frame = self.bgr_to_rbg(frame)

            # process frame and detect hands
            result = self.frame_process(rgb_frame)

            # recognize hand gesture
            gesture = self.hand_detection(result, frame)
            last_gesture = gesture

            # display gesture on screen
            cv2.putText(frame, f'Gesture: {gesture}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # show the output
            cv2.imshow("Hand Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                break

        cap.release()
        cv2.destroyAllWindows()

        # return the last movement executed
        return last_gesture


# if __name__ =="__main__":
#     recognizer = HandRecognition()
#     last_detected_gesture = recognizer.capture()
#     print(last_detected_gesture)

