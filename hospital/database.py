# hospital/database.py
import os
import json
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "hospital/database.json")

def load_db() -> dict:
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data: dict):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)