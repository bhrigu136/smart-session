"""
main.py

FastAPI entry point for SmartSession backend.
Responsible only for:
- app initialization
- routing
- WebSocket registration
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api.websocket import student_socket, teacher_socket
from app.api.health import health_check


def create_app() -> FastAPI:
    app = FastAPI(
        title="SmartSession Backend",
        description="Real-time student monitoring and engagement analysis",
        version="0.1.0"
    )

    # CORS for local frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # HTTP routes
    # -------------------------

    app.get("/health")(health_check)

    # -------------------------
    # WebSocket routes
    # -------------------------

    @app.websocket("/ws/student")
    async def ws_student(websocket: WebSocket):
        await student_socket(websocket)

    @app.websocket("/ws/teacher")
    async def ws_teacher(websocket: WebSocket):
        await teacher_socket(websocket)

    return app


app = create_app()
