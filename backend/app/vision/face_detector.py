"""
face_detector.py

Handles face and eye detection using OpenCV Haar Cascades.
Used strictly for integrity and simple geometric heuristics.
"""

import cv2
from typing import List, Tuple


class FaceDetector:
    """
    Thin wrapper around OpenCV Haar Cascade detection.

    Responsibilities:
    - Detect faces in a frame
    - Detect eyes within a detected face region
    - Return bounding boxes
    """

    def __init__(self):
        # Face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier.")

        # Eye detector
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

    def detect_faces(self, frame) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in a frame.

        Returns:
            List of bounding boxes (x, y, w, h) in FRAME coordinates.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        return faces.tolist() if len(faces) > 0 else []

    def detect_eyes(self, frame, face_box) -> List[Tuple[int, int, int, int]]:
        """
        Detect eyes within a detected face region.

        IMPORTANT:
        - Returned eye boxes are RELATIVE TO THE FACE ROI,
          not absolute frame coordinates.
        - This is intentional, as downstream logic only
          uses width/height ratios.
        """
        x, y, w, h = face_box
        face_roi = frame[y:y + h, x:x + w]
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

        eye_boxes_face_relative = self.eye_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )

        return (
            eye_boxes_face_relative.tolist()
            if len(eye_boxes_face_relative) > 0
            else []
        )

    def count_faces(self, frame) -> int:
        """
        Return number of detected faces in the frame.
        """
        return len(self.detect_faces(frame))
