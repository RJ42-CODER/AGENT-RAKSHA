from hospital.hospital_system import (
    get_patient,
    update_diagnosis,
    add_medication,
    schedule_appointment
)
import re

class HospitalAgent:
    def __init__(self,session):
        self.session = session

    def run(self,prompt:str ):
        prompt = prompt.lower()

        # 1: Show patient record
        if "show" in prompt and "record" in prompt:
            match = re.search(
                r"show (.*?) record",
                prompt
        )
            
        if match:
            patient_name = match.group(1).title()

            return self.view_patient(
                patient_name
            )
        
        return "Unknown Request"

    def view_patient(self,name):
        return get_patient(name,self.session)
    
    def update_patient(self,name,diagnosis):
        return update_diagnosis(name,diagnosis,self.session)
    
    def prescribe(self,name,medication):
        return add_medication(name,medication,self.session)
    
    def schedule(self,name,date,doctor):
        return schedule_appointment(name,date,doctor,self.schedule)
    


