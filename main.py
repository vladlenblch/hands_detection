import cv2

from core.detector import HandDetector
from core.drawer import HandDrawer

from ui.camera_window import CameraWindow

from recognizer.aggregator import HandGestureRecognizer

def main():
    hand_detector = HandDetector()
    hand_drawer = HandDrawer()
    camera_window = CameraWindow()

    recognizer = HandGestureRecognizer()
    
    while True:
        ret, frame = camera_window.read_frame()
 
        if ret:
            results = hand_detector.detect(frame)

            total_fingers = 0

            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    gesture_results = recognizer.process(landmarks=hand_landmarks)
                    total_fingers += gesture_results['fingers_count']

                    hand_drawer.draw(frame, hand_landmarks)

            cv2.putText(
                frame,
                f"Fingers: {total_fingers}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 0, 0),
                7,
                cv2.LINE_AA
            )
            
            camera_window.show(frame)
            
            if camera_window.wait_key() == ord('q'):
                break
    
    hand_detector.close()
    camera_window.close()

if __name__ == "__main__":
    main()
