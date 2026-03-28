from core.detector import HandDetector
from core.drawer import HandDrawer

from modes.manager import ModeManager
from modes.landmarks_only import LandmarksOnlyMode
from modes.finger_count import FingerCountMode
from modes.absolute_cinema import AbsoluteCinemaMode
from modes.help_me import HelpMeMode
from modes.six_seven import SixSevenMode

from core.camera_window import CameraWindow

def main():
    hand_detector = HandDetector()
    hand_drawer = HandDrawer()
    camera_window = CameraWindow()

    mode_manager = ModeManager(
        modes={
            0: LandmarksOnlyMode(),
            1: FingerCountMode(),
            2: AbsoluteCinemaMode(),
            3: HelpMeMode(),
            4: SixSevenMode()
        },
        default_mode_id=0,
    )
    
    while True:
        ret, frame = camera_window.read_frame()
 
        if ret:
            results = hand_detector.detect(frame)
            mode_manager.begin_frame()

            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    if mode_manager.current_mode_id == 0:
                        hand_drawer.draw(frame, hand_landmarks)
                    else:
                        mode_manager.process_hand(hand_landmarks)

            mode_manager.draw(frame)
            camera_window.show(frame)

            key = camera_window.wait_key()
            if key == ord('q'):
                break
            mode_manager.handle_key(key)
    
    hand_detector.close()
    camera_window.close()

if __name__ == "__main__":
    main()
