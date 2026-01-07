import time
from app.config import (
    CONFUSION_MIN_DURATION_SEC,
    CONFUSION_HEAD_TILT_THRESHOLD
)

class ConfusionDetector:
    def __init__(self):
        self._start_time = None
        self._confused = False

    def update(self, eye_strain: bool, head_tilt: float, gaze_centered: bool) -> bool:
        now = time.time()

        frame_confused = (
            gaze_centered and
            eye_strain and
            head_tilt > CONFUSION_HEAD_TILT_THRESHOLD
        )

        if frame_confused:
            if self._start_time is None:
                self._start_time = now
            elif now - self._start_time >= CONFUSION_MIN_DURATION_SEC:
                self._confused = True
        else:
            self._start_time = None
            self._confused = False
        return self._confused


    def reset(self):
        self._start_time = None
        self._confused = False

