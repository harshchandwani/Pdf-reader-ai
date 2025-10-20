import asyncio
from datetime import datetime, timedelta
import os

SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", 30))
CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL_SECONDS", 60))

async def cleanup_sessions(sessions: dict):
    """
    Background task to remove expired sessions and their PDF files.

    sessions: dict of session_id -> session_data
    Each session_data must have:
      - 'last_active': datetime (required)
      - 'pdf_path': str (optional, path to temp PDF file)
    """
    while True:
        now = datetime.now()
        expired_sessions = [
            sid for sid, data in sessions.items()
            if now - data.get("last_active", now) > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        ]

        for sid in expired_sessions:
            session_data = sessions.pop(sid, None)
            if not session_data:
                continue

            # Delete the temporary PDF file if it exists
            pdf_path = session_data.get("pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    print(f"[Session Cleanup] Deleted file for session {sid}: {pdf_path}")
                except Exception as e:
                    print(f"[Session Cleanup] Failed to delete {pdf_path}: {e}")

            print(f"[Session Cleanup] Session {sid} expired and removed")

        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
