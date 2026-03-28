import cv2

class ModeManager:
    def __init__(self, modes, default_mode_id=0):
        self.modes = modes
        self.current_mode_id = default_mode_id

    @property
    def current_mode(self):
        return self.modes[self.current_mode_id]

    def set_mode(self, mode_id):
        if mode_id not in self.modes or mode_id == self.current_mode_id:
            return

        self.current_mode.close()
        self.current_mode_id = mode_id

    def handle_key(self, key):
        if ord("0") <= key <= ord("9"):
            self.set_mode(int(chr(key)))

    def begin_frame(self):
        self.current_mode.begin_frame()

    def process_hand(self, landmarks):
        self.current_mode.process_hand(landmarks)

    def draw(self, frame):
        self.current_mode.draw_overlay(frame)
        self.draw_status(frame)

    def draw_status(self, frame):
        mode_label = f"Mode: {self.current_mode_id} - {self.current_mode.name}"
        controls_label = "0 Landmarks | 1 Finger Count | 2 Absolute Cinema | Q Quit"

        cv2.putText(frame, mode_label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (0, 0, 0), 10, cv2.LINE_AA)

        cv2.putText(frame, mode_label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (255, 255, 255), 5, cv2.LINE_AA)

        cv2.putText(frame, controls_label, (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (0, 0, 0), 10, cv2.LINE_AA)

        cv2.putText(frame, controls_label, (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1.8, (255, 255, 255), 5, cv2.LINE_AA)
