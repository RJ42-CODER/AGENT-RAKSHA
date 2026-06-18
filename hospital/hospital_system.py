# hospital/hospital_system.py
from hospital.database import load_db, save_db
from hospital.auth import verify_session
from hospital.users import USERS, PERMISSIONS
from hospital.audit import log_event

# load_dotenv()
# DB_PATH = os.getenv("DB_PATH","hospital/database.json")

# ===========================================================
# AUTH FUNCTIONS

def require_auth_session(session):
    if not verify_session(session):
        return "❌ Authentication Required"
    return None


def check_permission(role:str, action:str)-> bool:
    """
    Checks if a role is allowed to perform an action.
    """
    if role not in PERMISSIONS:
        return False
    return action in PERMISSIONS[role]

# READ operations:
# ├── get_patient(name)          → show patient record
# ├── list_all_patients()        → show all patients
# └── get_appointments()         → show today's schedule

# WRITE operations:
# ├── schedule_appointment()     → add new appointment
# ├── update_diagnosis()         → update patient diagnosis
# └── add_medication()           → add medication to patient

# SYSTEM operations:
# ├── get_hospital_status()      → show if system is locked
# └── emergency_alert(message)   → send emergency alert



# READ FUNCTIONS ->

def get_patient(name,session)-> str:
    """
    Returns patient record.
    DOCTOR + ADMIN: can view anyone
    PATIENT: can only view their own record
    RECEPTIONIST: cannot view medical records
    """
    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]
    current_user = session["username"]


    db = load_db()
    # check if system is locked
    if db["hospital"]["ransomware_active"]:
        return f"🔒 RECORDS LOCKED\n{db['hospital']['ransom_note']}"
    
    #checking permission
    if role == 'RECEPTIONIST':
        return "❌ Access Denied - Receptionists cannot view patient's medical records"
    
    if role == "PATIENT":
        # patients can only see their own record
        expected_name = current_user.replace("_"," ").title()
        if name.lower() != expected_name.lower():
            return f"❌ Access Denied! - You can view your own records only."
        
    if not check_permission(role,"read") and role != "PATIENT":
        return f"❌ Access Denied! - Insufficient permissions."
    
    #find patient - all passed

    for patient in db["patients"]:
        if patient["name"].lower() == name.lower():

            log_event(
                user=current_user,
                action="VIEW_PATIENT",
                target=patient["name"]
                )
            return f"""
╔══════════════════════════════════════╗
║         PATIENT RECORD               ║
╚══════════════════════════════════════╝
ID:           {patient['id']}
Name:         {patient['name']}
Age:          {patient['age']}
Blood Type:   {patient['blood_type']}
Diagnosis:    {patient['diagnosis']}
Medications:  {', '.join(patient['medications'])}
Appointments: {', '.join(patient['appointments'])}
"""
        
    
    return f"❌ Patient '{name}'not found"


def list_all_patients(session)->str:
    """
    Lists all patients.
    DOCTOR + ADMIN only.
    """

    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]

    db = load_db()

    if db["hospital"]["ransomware_active"]:
        return f"🔒 RECORDS LOCKED\n{db['hospital']['ransom_note']}"
    
    if not check_permission(role,"read"):
        return f"❌ Access Denied - Only Doctors and Admins can list all patients"
    
    result = "╔══════════════════════════════════════╗\n"
    result += "║         ALL PATIENTS                 ║\n"
    result += "╚══════════════════════════════════════╝\n"

    for p in db["patients"]:
        result += f"• {p['name']} (Age: {p['age']})- {p['diagnosis']}\n"

    
    log_event(
    user=session["username"],
    action="LIST_ALL_PATIENTS",
    target="ALL_PATIENTS"

    )

    return result

def get_appointments(session) -> str:
    """
    Lists all appointments.
    DOCTOR + ADMIN + RECEPTIONIST can view.
    """

    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]
    
    db = load_db()

    if db["hospital"]["ransomware_active"]:
        return f"🔒 SYSTEM LOCKED\n{db['hospital']['ransom_note']}"
    
    if not check_permission(role,"read") and not check_permission(role,"schedule"):
        return "❌ Access Denied"
    
    result = "╔══════════════════════════════════════╗\n"
    result += "║         APPOINTMENTS                 ║\n"
    result += "╚══════════════════════════════════════╝\n"

    for p in db["patients"]:
        for appt in p["appointments"]:
            result += f"• {p['name']}: {appt}\n"

    log_event(
    user=session["username"],
    action="VIEW_APPOINTMENTS",
    target="SCHEDULE"
    )
    
    return result

# WRITE FUNCTIONS
# ============================================================

def schedule_appointment(name:str, date:str, doctor:str, session)->str:
    """
    Schedules appointment.
    RECEPTIONIST + DOCTOR + ADMIN only.
    """
    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]

    db = load_db()

    if db["hospital"]["ransomware_active"]:
        return f"🔒 SYSTEM LOCKED\n{db['hospital']['ransom_note']}"
    
    if not check_permission(role,"schedule") and not check_permission(role, "write"):
        return "❌ Access Denied — Cannot schedule appointments"
    
    for patient in db["patients"]:
        if patient["name"].lower() == name.lower():
            appointment = f"{date} - {doctor}"
            patient["appointments"].append(appointment)
            save_db(db)

            log_event(
                user=session["username"],
                action="SCHEDULE_APPOINTMENTS",
                target=patient["name"],
                details=f"{date} | {doctor}"
                )

            return f"✅ Appointment scheduled for {name} on {date} with {doctor}"
        
    return f"❌ Patient '{name}' not found"

def update_diagnosis(name:str, diagnosis:str, session)-> str:
    """
    Updates patient diagnosis.
    DOCTOR + ADMIN only.
    """

    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]

    db = load_db()

    if db["hospital"]["ransomware_active"]:
        return f"🔒 SYSTEM LOCKED\n{db['hospital']['ransom_note']}"
    
    if not check_permission(role,"write"):
        return "❌ Access Denied — Only Doctors and Admins can update diagnoses"
    
    for patient in db["patients"]:
        if patient["name"].lower() == name.lower():
            old_diagnosis = patient["diagnosis"]
            patient["diagnosis"] = diagnosis
            save_db(db)

            log_event(
                user=session["username"],
                action="UPDATE_DIAGNOSIS",
                target=patient["name"],
                details= f"{old_diagnosis} -> {diagnosis}"
                )
            
            return f"✅ Diagnosis updated for {name}\nPrevious: {old_diagnosis}\nNew: {diagnosis}"

        
    return f"❌ Patient '{name}' not found"


def add_medication(name:str,medication:str,session) ->str:
    """
    Adds medication to patient.
    DOCTOR + ADMIN only.
    """
    error = require_auth_session(session)
    if error:
        return error
    
    role = session["role"]

    db = load_db()

    if db["hospital"]["ransomware_active"]:
        return f"🔒 SYSTEM LOCKED\n{db['hospital']['ransom_note']}"
    
    if not check_permission(role,"write"):
        return "❌ Access Denied — Only Doctors and Admins can add medications"
    
    for patient in db["patients"]:
        if patient["name"].lower() == name.lower():
            patient["medications"].append(medication)
            save_db(db)
            log_event(
                user=session["username"],
                action="ADD_MEDICATION",
                target=patient["name"],
                details= medication
                )
            return f"✅ Medication '{medication}' added for {name}"

    return f"❌ Patient '{name}' not found"

# SYSTEM FUNCTIONS
# ============================================================

def get_hospital_status()->dict:
    """
    Returns current hospital system status.
    """
    db = load_db()
    return{
        "hospital_name": db["hospital"]["name"],
        "ransomware_active": db["hospital"]["ransomware_active"],
        "ransom_note": db["hospital"]["ransom_note"],
        "total_patients": len(db["patients"]),
        "status": "🔒 LOCKED" if db["hospital"]["ransomware_active"] else "✅ OPERATIONAL"
    }

