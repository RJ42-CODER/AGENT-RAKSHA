# USERS & ROLES

USERS = {
    "dr_mehta": {"password":"doc@123","role":"DOCTOR"},
    "dr_kapoor": {"password":"doc@456", "role":"DOCTOR"},
    "reception1":   {"password": "rec123",   "role": "RECEPTIONIST"},
    "reception2":   {"password": "rec456",   "role": "RECEPTIONIST"},
    "admin":        {"password": "admin123", "role": "ADMIN"},
    "priya_sharma": {"password": "pat123",   "role": "PATIENT"},
    "rahul_mehta":  {"password": "pat456",   "role": "PATIENT"},
    "ananya_iyer":  {"password": "pat789",   "role": "PATIENT"}
}

PERMISSIONS = {
    "ADMIN": ["read","write","schedule","system"],
    "DOCTOR": ["read","write"],
    "RECEPTIONIST": ["schedule","read_basic"],
    "PATIENT": ["read_own"]
}