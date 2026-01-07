"""
health.py

Simple health check endpoint.
Used to verify backend is running.
"""

def health_check():
    return {"status": "ok"}
