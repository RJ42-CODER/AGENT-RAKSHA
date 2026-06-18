# hospital/auth.py
import uuid
from hospital.users import USERS

ACTIVE_SESSIONS = {}

def login(username: str, password: str):
    username = username.lower()
    if username not in USERS:
        return None
    if USERS[username]["password"] != password:
        return None
    session = {
        "session_id":    str(uuid.uuid4()),
        "authenticated": True,
        "username":      username,
        "role":          USERS[username]["role"]
    }
    ACTIVE_SESSIONS[username] = session
    return session

def verify_session(session):
    if not session:
        return False
    session_id = session.get("session_id")
    if not session_id:
        return False
    username = session.get("username")
    if username not in ACTIVE_SESSIONS:
        return False
    stored = ACTIVE_SESSIONS[username]
    return stored["session_id"] == session_id

def logout(session):
    username = session.get("username")
    if username in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[username]
    return True