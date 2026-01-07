import time
from enum import Enum

class StudentStatus(Enum):
    FOCUSED = "focused"
    CONFUSED = "confused"
    PROCTOR_ALERT = "proctor_alert"

class SessionState:

    def __init__(self, gaze_away_threshold_sec: float):
        self.gaze_away_threshold_sec = gaze_away_threshold_sec

        self._last_gaze_centered_time = time.time()
        self._face_missing_since = None
        self._multi_face_detected = False

        self.current_status = StudentStatus.FOCUSED

    
    # Gaze tracking for longer than threshold, proctor alert will be raised.
    def update_gaze(self, gaze_centered: bool):
        now = time.time()

        if gaze_centered:
            self._last_gaze_centered_time = now
        elif (now - self._last_gaze_centered_time) >= self.gaze_away_threshold_sec:
            self.current_status = StudentStatus.PROCTOR_ALERT

    
    # Face presence
    def update_face_count(self, face_count: int):
        now = time.time()

        if face_count == 1:
            self._face_missing_since = None
            self._multi_face_detected = False

        elif face_count == 0:
            if self._face_missing_since is None:
                self._face_missing_since = now
            else:
                self.current_status = StudentStatus.PROCTOR_ALERT

        else:
            self._multi_face_detected = True
            self.current_status = StudentStatus.PROCTOR_ALERT

    
    # Engagement state
    def update_confusion(self, is_confused: bool):
        if self.current_status == StudentStatus.PROCTOR_ALERT:
            return

        if is_confused:
            self.current_status = StudentStatus.CONFUSED
        else:
            self.current_status = StudentStatus.FOCUSED

    
    # Public interface
    def snapshot(self) -> dict:
        return {
            "status": self.current_status.value,
            "timestamp": time.time()
        }

    def reset(self):
        
        # Resets session to default state.
        
        self._last_gaze_centered_time = time.time()
        self._face_missing_since = None
        self._multi_face_detected = False
        self.current_status = StudentStatus.FOCUSED



