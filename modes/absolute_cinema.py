import random
import cv2
import os

from recognizer.finger_counter import FingerCounter
from modes.base import BaseMode

class AbsoluteCinemaMode(BaseMode):
    def __init__(self):
        self.name = "Absolute Cinema"
        self.finger_counter = FingerCounter()
        self.total_fingers = 0
        self.image_paths = [
            os.path.join("assets/absolute_cinema", filename)
            for filename in os.listdir("assets/absolute_cinema")
            if filename.endswith(".png")
        ]
        self.is_showing_image = False
        self.current_image = None
    
    def begin_frame(self):
        self.total_fingers = 0
    
    def process_hand(self, landmarks):
        self.total_fingers += self.finger_counter.detect(landmarks)

    def draw_overlay(self, frame):
        if self.total_fingers == 10:
            if not self.is_showing_image and self.image_paths:
                image_path = random.choice(self.image_paths)
                self.current_image = cv2.imread(image_path)

                if self.current_image is not None:
                    cv2.imshow("Absolute Cinema", self.current_image)
                    cv2.moveWindow("Absolute Cinema", 300, 150)
                    self.is_showing_image = True
        else:
            self.close()

    def close(self):
        if self.is_showing_image:
            cv2.destroyWindow("Absolute Cinema")
            self.is_showing_image = False
            self.current_image = None
