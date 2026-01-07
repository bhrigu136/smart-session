# Simple health check endpoint. Used for verify backend is running.

def health_check():
    return {"status": "ok"}
