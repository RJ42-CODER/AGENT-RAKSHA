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
from hospital.hospital_agent import HospitalAgent

session = login(
    "dr_mehta",
    "doc@123"
)

agent = HospitalAgent(session)

print(
    agent.run(
        "Show Priya Sharma record"
    )
)