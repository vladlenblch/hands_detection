from .finger_counter import FingerCounter

class HandGestureRecognizer:
    def __init__(self):
        self.finger_counter = FingerCounter()
    
        self.frame_count = 0
    
    def process(self, landmarks):
        gesture_results = {
            'frame': self.frame_count,
            'fingers_count': self.finger_counter.detect(landmarks)
        }

        self.frame_count += 1

        return gesture_results
    
    def reset(self):
        self.frame_count = 0
        self.finger_counter.reset()
