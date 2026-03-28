import cv2
import os

from recognizer.geometry import calculate_distance
from recognizer.finger_counter import FingerCounter
from modes.base import BaseMode

class MemesMode(BaseMode):
    def __init__(self):
        self.name = "Memes"
        self.finger_counter = FingerCounter()
        self.total_fingers = 0
        self.image_paths = [
            os.path.join("assets/memes", filename)
            for filename in sorted(os.listdir("assets/memes"))
            if filename.endswith((".png", ".jpg", ".jpeg"))
        ]
        self.current_index = 0
        self.is_showing_image = False
        self.current_image = None
        self.is_pinching = False
        self.pinch_detected = False
    
    def begin_frame(self):
        self.total_fingers = 0
        self.pinch_detected = False
    
    def process_hand(self, landmarks):
        self.total_fingers += self.finger_counter.detect(landmarks)
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        if calculate_distance(thumb_tip, index_tip) < 0.05:
            self.pinch_detected = True
    
    def draw_overlay(self, frame):
        if not self.is_showing_image:
            image_path = self.image_paths[self.current_index]
            self.current_image = cv2.imread(image_path)

            if self.current_image is not None:
                image_height, image_width = self.current_image.shape[:2]
                cv2.imshow("Memes", self.current_image)
                cv2.moveWindow("Memes", (1512 - image_width) // 2, (982 - image_height) // 2)
                self.is_showing_image = True

        if self.pinch_detected and not self.is_pinching:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            image_path = self.image_paths[self.current_index]
            self.current_image = cv2.imread(image_path)

            if self.current_image is not None:
                image_height, image_width = self.current_image.shape[:2]
                cv2.imshow("Memes", self.current_image)
                cv2.moveWindow("Memes", (1512 - image_width) // 2, (982 - image_height) // 2)
                self.is_showing_image = True

        self.is_pinching = self.pinch_detected

    
    def close(self):
        if self.is_showing_image:
            cv2.destroyWindow("Memes")
            self.is_showing_image = False
            self.current_image = None
        self.is_pinching = False
        self.pinch_detected = False
