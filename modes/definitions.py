import cv2

from recognizer.aggregator import HandGestureRecognizer

class BaseMode:
    def __init__(self):
        self.name = "Base"

    def begin_frame(self):
        pass

    def process_hand(self, landmarks):
        pass

    def draw_overlay(self, frame):
        pass

class LandmarkOnlyMode(BaseMode):
    def __init__(self):
        self.name = "Landmarks"

class FingerCountMode(BaseMode):
    def __init__(self):
        self.name = "Finger Count"
        self.recognizer = HandGestureRecognizer()
        self.total_fingers = 0

    def begin_frame(self):
        self.total_fingers = 0

    def process_hand(self, landmarks):
        gesture_results = self.recognizer.process(landmarks)
        self.total_fingers += gesture_results["fingers_count"]

    def draw_overlay(self, frame):
        label = f"Fingers: {self.total_fingers}"

        cv2.putText(frame, label, (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (0, 0, 0), 10, cv2.LINE_AA)

        cv2.putText(frame, label, (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (255, 255, 255), 5, cv2.LINE_AA)
