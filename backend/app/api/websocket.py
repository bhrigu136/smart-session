import json
import base64
from fastapi import WebSocket, WebSocketDisconnect

from app.state.session_state import SessionState
from app.vision.face_detector import FaceDetector
from app.vision.gaze_tracker import GazeTracker, GazeDirection
from app.vision.confusion_logic import ConfusionDetector
from app.vision.emotion_features import extract_emotion_features
from app.config import GAZE_AWAY_THRESHOLD_SEC


class ConnectionManager:
    def __init__(self):
        self.students = []
        self.teachers = []

    async def connect_student(self, websocket: WebSocket):
        await websocket.accept()
        self.students.append(websocket)

    async def connect_teacher(self, websocket: WebSocket):
        await websocket.accept()
        self.teachers.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.students:
            self.students.remove(websocket)
        if websocket in self.teachers:
            self.teachers.remove(websocket)

    async def broadcast_to_teachers(self, message: dict):
        for teacher in list(self.teachers):
            try:
                await teacher.send_json(message)
            except Exception:
                self.teachers.remove(teacher)

manager = ConnectionManager()


def decode_frame(frame_b64: str):
    """
    Decode base64 image strings into OpenCV frame.
    """
    img_bytes = base64.b64decode(frame_b64)
    import numpy as np
    import cv2

    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)



# websocket endpoints
async def student_socket(websocket: WebSocket):
    # Receive video frames from student, process them, and broadcasts to teacher.
    
    await manager.connect_student(websocket)

    session_state = SessionState(
        gaze_away_threshold_sec=GAZE_AWAY_THRESHOLD_SEC
    )
    face_detector = FaceDetector()
    gaze_tracker = GazeTracker(GAZE_AWAY_THRESHOLD_SEC)
    confusion_detector = ConfusionDetector()

    try:
        while True:
            payload = await websocket.receive_text()
            data = json.loads(payload)

            # basics payload validation
            if "frame" not in data or "gaze_direction" not in data:
                continue

            
            # Decode frame
            frame = decode_frame(data["frame"])
            
            # Integrity: face count
            faces = face_detector.detect_faces(frame)
            face_count = len(faces)
            session_state.update_face_count(face_count)

            
            # Integrity: gaze tracking
            gaze_direction = GazeDirection(data["gaze_direction"])
            gaze_tracker.update(gaze_direction)

            session_state.update_gaze(
                gaze_centered=(gaze_direction == GazeDirection.CENTER)
            )

            
            # Engagement: confusion detection
            is_confused = False

            if face_count == 1:
                face_box = faces[0]
                eyes = face_detector.detect_eyes(frame, face_box)

                features = extract_emotion_features(face_box, eyes)

                is_confused = confusion_detector.update(
                    eye_strain=features["eye_strain"],
                    head_tilt=features["head_tilt"],
                    gaze_centered=(gaze_direction == GazeDirection.CENTER)
                )

            session_state.update_confusion(is_confused)

            # Broadcast snapshot
            snapshot = session_state.snapshot()
            snapshot["gaze_direction"] = gaze_tracker.current_direction
            snapshot["face_count"] = face_count

            await manager.broadcast_to_teachers(snapshot)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def teacher_socket(websocket: WebSocket):
    await manager.connect_teacher(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
