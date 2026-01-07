"""
gaze_tracker.py

Tracks gaze direction duration for proctoring.
Gaze direction itself is provided by the frontend.
This module is responsible ONLY for time-based integrity checks.
"""

import time
from enum import Enum


class GazeDirection(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class GazeTracker:
    """
    Maintains temporal state for gaze-based proctoring.

    A proctor alert is raised only if the student
    continuously looks away from the screen
    for longer than the configured threshold.
    """

    def __init__(self, away_threshold_sec: float):
        self.away_threshold_sec = away_threshold_sec
        self._last_centered_time = time.time()
        self._current_direction = GazeDirection.CENTER

    def update(self, direction: GazeDirection) -> bool:
        """
        Update gaze direction and check for violation.

        Args:
            direction (GazeDirection): Current gaze direction
                                       provided by frontend.

        Returns:
            bool: True if gaze-away duration exceeds threshold.
        """
        now = time.time()
        self._current_direction = direction

        if direction == GazeDirection.CENTER:
            self._last_centered_time = now
            return False

        away_duration = now - self._last_centered_time
        return away_duration >= self.away_threshold_sec

    @property
    def current_direction(self) -> str:
        """
        Returns current gaze direction as string.
        """
        return self._current_direction.value

    def reset(self):
        """
        Reset gaze tracking state.
        """
        self._last_centered_time = time.time()
        self._current_direction = GazeDirection.CENTER
