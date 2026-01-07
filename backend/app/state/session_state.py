"""
session_state.py

Maintains temporal session state for a single student.
All integrity and engagement decisions depend on this state.
"""

import time
from enum import Enum


class StudentStatus(Enum):
    FOCUSED = "focused"
    CONFUSED = "confused"
    PROCTOR_ALERT = "proctor_alert"


class SessionState:
    """
    Tracks temporal signals across video frames.

    This class intentionally stores time-based context
    instead of making per-frame decisions.
    """

    def __init__(self, gaze_away_threshold_sec: float):
        self.gaze_away_threshold_sec = gaze_away_threshold_sec

        self._last_gaze_centered_time = time.time()
        self._face_missing_since = None
        self._multi_face_detected = False

        self.current_status = StudentStatus.FOCUSED

    # -------------------------
    # Gaze tracking
    # -------------------------

    def update_gaze(self, gaze_centered: bool):
        """
        Updates gaze state.

        If gaze is away for longer than threshold,
        proctor alert will be raised.
        """
        now = time.time()

        if gaze_centered:
            self._last_gaze_centered_time = now
        elif (now - self._last_gaze_centered_time) >= self.gaze_away_threshold_sec:
            self.current_status = StudentStatus.PROCTOR_ALERT

    # -------------------------
    # Face presence
    # -------------------------

    def update_face_count(self, face_count: int):
        """
        Updates face presence state.
        """
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

    # -------------------------
    # Engagement state
    # -------------------------

    def update_confusion(self, is_confused: bool):
        """
        Updates engagement state if no proctor alert exists.
        """
        if self.current_status == StudentStatus.PROCTOR_ALERT:
            return

        if is_confused:
            self.current_status = StudentStatus.CONFUSED
        else:
            self.current_status = StudentStatus.FOCUSED

    # -------------------------
    # Public interface
    # -------------------------

    def snapshot(self) -> dict:
        """
        Returns a serializable snapshot of the session state.
        """
        return {
            "status": self.current_status.value,
            "timestamp": time.time()
        }

    def reset(self):
        """
        Resets session to default state.
        """
        self._last_gaze_centered_time = time.time()
        self._face_missing_since = None
        self._multi_face_detected = False
        self.current_status = StudentStatus.FOCUSED
