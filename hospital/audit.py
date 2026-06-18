# hospital/audit.py
from datetime import datetime
from hospital.database import load_db, save_db

def log_event(user: str, action: str, target: str, 
              status: str = "SUCCESS", details: str = ""):
    db = load_db()
    event = {
        "timestamp": datetime.now().isoformat(),
        "user":      user,
        "action":    action,
        "target":    target,
        "status":    status,
        "details":   details
    }
    db["audit_logs"].append(event)
    save_db(db)

def get_logs():
    db = load_db()
    return db.get("audit_logs", [])

def print_logs():
    logs = get_logs()
    if not logs:
        print("No audit logs found.")
        return
    print("\n===== AUDIT LOGS =====\n")
    for log in logs:
        print(f"[{log['timestamp']}] {log['user']} | {log['action']} | {log['target']} | {log['status']}")
        if log["details"]:
            print(f"   Details: {log['details']}")
        print("-" * 60)