import sys
import os

from core.hand_detector import HandDetector
from core.hand_drawer import HandDrawer
from ui.camera_window import CameraWindow

def main():
    hand_detector = HandDetector()
    hand_drawer = HandDrawer()
    camera_window = CameraWindow()
    
    while True:
        ret, frame = camera_window.read_frame()
 
        if ret:
            results = hand_detector.detect(frame)

            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    hand_drawer.draw(frame, hand_landmarks)
            
            camera_window.show(frame)
            
            if camera_window.wait_key() == ord('q'):
                break
    
    hand_detector.close()
    camera_window.close()

if __name__ == "__main__":
    main()
