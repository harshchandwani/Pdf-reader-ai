# session_cleanup.py
import asyncio
from datetime import datetime, timedelta
import os

SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", 30))
CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL_SECONDS", 60))

async def cleanup_sessions(sessions: dict):
    """
    Background task to remove expired sessions.
    sessions: dict of session_id -> session_data
    Each session_data should have a 'last_active' datetime.
    """
    while True:
        now = datetime.now()
        expired_sessions = [
            sid for sid, data in sessions.items()
            if now - data.get("last_active", now) > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        ]
        for sid in expired_sessions:
            del sessions[sid]
            print(f"[Session Cleanup] Session {sid} expired and removed")
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
