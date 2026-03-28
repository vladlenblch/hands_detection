import os
import pygame

from recognizer.finger_counter import FingerCounter
from recognizer.geometry import calculate_distance
from modes.base import BaseMode

class RockMode(BaseMode):
    def __init__(self):
        self.name = "Rock"
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.finger_counter = FingerCounter()
        self.is_rock_gesture = False
        self.song_paths = [
            os.path.join("assets/songs", filename)
            for filename in os.listdir("assets/songs")
            if filename.endswith((".mp3", ".wav"))
        ]
        self.current_index = -1
        self.is_playing_song = False
        self.was_rock_gesture = False
    
    def begin_frame(self):
        self.is_rock_gesture = False
    
    def process_hand(self, landmarks):
        if self.is_rock_hand(landmarks):
            self.is_rock_gesture = True

    def draw_overlay(self, frame):
        if self.is_rock_gesture and not self.was_rock_gesture:
            self.current_index = (self.current_index + 1) % len(self.song_paths)
            self.play_current_song()

        self.was_rock_gesture = self.is_rock_gesture
    
    def close(self):
        if self.is_playing_song:
            pygame.mixer.music.stop()
            self.is_playing_song = False
        self.was_rock_gesture = False
    
    def play_current_song(self):
        song_path = self.song_paths[self.current_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.is_playing_song = True

    def is_rock_hand(self, landmarks):
        return (
            self.is_finger_up(landmarks, "index") and
            not self.is_finger_up(landmarks, "middle") and
            not self.is_finger_up(landmarks, "ring") and
            self.is_finger_up(landmarks, "pinky")
        )

    def is_finger_up(self, landmarks, finger_name):
        wrist = landmarks[self.finger_counter.wrist_id]

        tip_id = self.finger_counter.finger_ids[finger_name]["tip"]
        pip_id = self.finger_counter.finger_ids[finger_name]["pip"]
        mcp_id = self.finger_counter.finger_ids[finger_name]["mcp"]

        tip = landmarks[tip_id]
        pip = landmarks[pip_id]
        mcp = landmarks[mcp_id]

        dist_tip_wrist = calculate_distance(tip, wrist)
        dist_pip_wrist = calculate_distance(pip, wrist)
        dist_mcp_wrist = calculate_distance(mcp, wrist)

        return dist_tip_wrist > dist_pip_wrist * 1.2 and dist_tip_wrist > dist_mcp_wrist
