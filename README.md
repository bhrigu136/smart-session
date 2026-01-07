# Smart Session – Real-Time Confusion Detection & Proctoring System

## Overview

**Smart Session** is a real-time classroom monitoring prototype that detects **student confusion** and **proctoring violations** during live online sessions.

The system analyzes a student’s video stream in real time and sends live session telemetry to a teacher dashboard using **WebSockets**.
All detection logic is **rule-based and explainable**, prioritizing transparency and stability over black-box models.

This project was built as part of the **nSkills AI Internship Assignment**.

---

## Key Objectives

* Detect when a student appears **confused** during a live session
* Monitor **proctoring integrity** (gaze diversion, multiple people)
* Provide **real-time updates** to a teacher dashboard
* Keep logic **interpretable**, **modular**, and **lightweight**

---

## System Architecture

**High-level flow:**

```
Student Camera
     ↓
WebSocket (Student)
     ↓
FastAPI Backend
  - Face Detection
  - Gaze Tracking
  - Confusion Logic
  - Session State
     ↓
WebSocket (Teacher)
     ↓
Teacher Dashboard
```

* The backend is the **source of truth**
* Frontend sends raw inputs only (video frame and estimated gaze direction)
* All decision logic happens server-side

---

## Technologies Used

### Backend

* **FastAPI** – backend framework
* **WebSockets** – real-time communication
* **Uvicorn** – ASGI server

### Computer Vision

* **OpenCV (Haar Cascades)** – face & eye detection
* **NumPy** – numerical operations

---

## Proctoring (Integrity) Logic

### Face Validation

* **0 faces detected** → violation
* **More than 1 face** → violation

### Gaze Tracking

* Gaze direction is provided by the frontend
* Backend tracks **continuous gaze-away duration**
* If gaze is away from center for **> 4 seconds**, a proctor alert is raised

This separation reduces backend CV load while keeping integrity enforcement server-side.

---

## Confusion Detection Logic (Custom & Explainable)

Confusion is detected using **simple geometric heuristics**, not emotion classifiers.

A student is marked **confused** if **all** of the following persist:

1. Gaze is centered (student is looking at screen)
2. Eye strain detected

   * Based on eye height-to-width ratio
3. Head tilt exceeds threshold

   * Indicates cognitive uncertainty
4. Conditions persist for a minimum duration (temporal validation)

This avoids false positives caused by momentary expressions.

---

##  Temporal Reasoning

All critical decisions are **time-aware**:

* Gaze violations require continuous duration
* Confusion is detected only if signals persist
* Momentary noise is ignored

This makes the system robust in real-world usage.

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── websocket.py
│   │   └── health.py
│   ├── vision/
│   │   ├── face_detector.py
│   │   ├── gaze_tracker.py
│   │   ├── confusion_logic.py
│   │   └── emotion_features.py
│   ├── state/
│   │   └── session_state.py
│   ├── config.py
│   └── main.py
├── run.py
└── requirements.txt
```

Each module has a **single responsibility**.

---

## How to Run the Project

### 1️ Create virtual environment

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2️ Install dependencies

```
pip install -r requirements.txt
```

### 3️ Start backend server

```
cd backend
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

### 4️ Health check

Visit:

```
http://127.0.0.1:8000/health
```

Expected response:

```
{"status": "ok"}
```

---

## Known Limitations (Intentional)

* No deep learning emotion models (by design)
* Confusion detection uses heuristic proxies
* Frontend UI is minimal (prototype-level)
* No database or session persistence

These choices were made to prioritize **clarity, explainability, and stability** for an MVP.

---

## Conclusion

This project demonstrates:

* real-time system design
* interpretable computer vision
* clean backend architecture
* practical trade-offs for production-ready prototypes

It satisfies all requirements of the assignment while remaining easy to explain and extend.

---

## Author

**Tamanna Bhrigunath**
Poornima College of Engineering
B.Tech – AI & Data Science
2026 Batch
