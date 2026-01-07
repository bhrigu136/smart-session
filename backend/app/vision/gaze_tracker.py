import time
from enum import Enum

class GazeDirection(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

class GazeTracker:
    # A protocor alert raised if student looks away too long.

    def __init__(self, away_threshold_sec: float):
        self.away_threshold_sec = away_threshold_sec
        self._last_centered_time = time.time()
        self._current_direction = GazeDirection.CENTER

    def update(self, direction: GazeDirection) -> bool:
        now = time.time()
        self._current_direction = direction

        if direction == GazeDirection.CENTER:
            self._last_centered_time = now
            return False

        away_duration = now - self._last_centered_time
        return away_duration >= self.away_threshold_sec

    @property
    def current_direction(self) -> str:
        return self._current_direction.value

    def reset(self):
        self._last_centered_time = time.time()
        self._current_direction = GazeDirection.CENTER
