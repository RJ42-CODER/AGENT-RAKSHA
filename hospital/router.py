import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

TOOLS_DESCRIPTION = """You are a JSON-only routing API. You must ONLY respond with a single JSON object. No explanation. No text. No markdown. Just JSON.

Available tools:
- view_patient: view one patient record. Arguments: {"name": "string"}
- list_all_patients: list all patients. Arguments: {}
- schedule_appointment: schedule appointment. Arguments: {"name": "string", "date": "string", "doctor": "string"}
- update_diagnosis: update diagnosis. Arguments: {"name": "string", "diagnosis": "string"}
- add_medication: add medication. Arguments: {"name": "string", "medication": "string"}
- get_appointments: view all appointments. Arguments: {}
- get_hospital_status: check system status. Arguments: {}

RULES:
- ONLY respond with JSON
- NEVER explain anything
- NEVER ask questions
- ALWAYS pick the closest matching tool

EXAMPLES:
Input: Show Priya Sharma record
Output: {"tool": "view_patient", "arguments": {"name": "Priya Sharma"}}

Input: List all patients
Output: {"tool": "list_all_patients", "arguments": {}}

Input: Schedule Rahul for July 5th with Dr Singh
Output: {"tool": "schedule_appointment", "arguments": {"name": "Rahul Mehta", "date": "2025-07-05", "doctor": "Dr. Singh"}}

Input: What is hospital status
Output: {"tool": "get_hospital_status", "arguments": {}}

Input: Add Paracetamol for Priya
Output: {"tool": "add_medication", "arguments": {"name": "Priya Sharma", "medication": "Paracetamol"}}"""

def route(prompt:str) -> dict:
    """
    Sends prompt to LLM and gets back tool + arguments.
    Returns:
      - tool      : function name to call
      - arguments : dict of arguments
      - raw       : raw LLM response
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ← bigger model, follows instructions better
            messages=[
                {"role": "system", "content": TOOLS_DESCRIPTION},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=100,
            temperature=0    # ← 0 = deterministic, no creativity, just follow instructions
)

        raw = response.choices[0].message.content.strip()
        # print(f"DEBUG RAW: {raw}")

        # clean any markdown backticks if LLM adds them
        raw = raw.replace("```json", "").replace("```", "").strip()
        decision = json.loads(raw)

        return {
            "success": True,
            "tool": decision.get("tool","unknown"),
            "arguments": decision.get("arguments",{}),
            "raw": raw
        }
    except Exception as e:
        # print(f"DEBUG ERROR: {e}") 
        return{
            "success":False,
            "tool":"unknown",
            "arguments":{},
            "error":str(e)
        }


