# tests/test_router.py
from hospital.router import route

prompts = [
    "Show Priya Sharma record",
    "Can you retrieve Rahul Mehta medical information?",
    "Schedule Ananya for July 5th with Dr Singh",
    "List all patients in the hospital",
    "What is the hospital status?",
    "Add medication Paracetamol for Priya Sharma",
]

print("=== LLM Router Tests ===\n")

for p in prompts:
    result = route(p)
    print(f"Prompt: {p}")
    print(f"Tool:   {result['tool']}")
    print(f"Args:   {result['arguments']}")
    print()