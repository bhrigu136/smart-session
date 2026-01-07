import cv2
import math


def compute_eye_aspect_ratio(eye_box):
    x, y, w, h = eye_box
    if w == 0:
        return 0.0
    return h / w


def compute_head_tilt(left_eye, right_eye):
    lx, ly, lw, lh = left_eye
    rx, ry, rw, rh = right_eye

    left_center = (lx + lw / 2, ly + lh / 2)
    right_center = (rx + rw / 2, ry + rh / 2)

    dx = right_center[0] - left_center[0]
    dy = right_center[1] - left_center[1]

    if dx == 0:
        return 0.0

    return math.degrees(math.atan2(dy, dx))


def extract_emotion_features(face, eyes):

    features = {
        "eye_strain": False,
        "head_tilt": 0.0
    }

    if len(eyes) >= 2:
        left_eye, right_eye = eyes[:2]

        ear_left = compute_eye_aspect_ratio(left_eye)
        ear_right = compute_eye_aspect_ratio(right_eye)

        features["eye_strain"] = (ear_left < 0.25 and ear_right < 0.25)
        features["head_tilt"] = abs(
            compute_head_tilt(left_eye, right_eye)
        )

    return features



