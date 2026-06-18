import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from hospital.auth import login
from hospital.hospital_system import (
    get_patient,
    list_all_patients,
    schedule_appointment,
    update_diagnosis,
    add_medication
)
from hospital.audit import print_logs


# Login
session = login("dr_mehta", "doc@123")

print(session)

print("\n" + "="*50)

# Read Patient
print(get_patient("Priya Sharma", session))

print("\n" + "="*50)

# Update Diagnosis
print(update_diagnosis(
    "Priya Sharma",
    "Pneumonia",
    session
))

print("\n" + "="*50)

# Add Medication
print(add_medication(
    "Priya Sharma",
    "Azithromycin 500mg",
    session
))

print("\n" + "="*50)

# Schedule Appointment
print(schedule_appointment(
    "Priya Sharma",
    "2025-07-10 10:00 AM",
    "Dr. Mehta",
    session
))

print("\n" + "="*50)

# Audit Logs
print_logs()