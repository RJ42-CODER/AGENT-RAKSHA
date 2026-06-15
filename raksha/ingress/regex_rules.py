# regress is regular expression like finding patterns in a text.

# Normal search: finds exact word "delete"
# Regex search: finds "delete", "DELETE", "d e l e t e", "d3lete" all at once

import re

# ATTACK PATTERNS
# Each pattern has:
#   - "pattern"     : the regex to search for
#   - "description" : what attack this catches
#   - "severity"    : how dangerous it is (high/medium)


ATTACK_PATTERNS = [
    {
        "pattern": r"ignore\s+(all\s+)?(your\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?|context)",
        "description": "Direct prompt injection - instruction override",
        "severity": "high"
    },
    {
        "pattern": r"forget\s+(all\s+)?(your\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?|context)",
        "description": "Direct prompt injection - memory wipe attempt",
        "severity": "high"
    },
    {
        "pattern": r"you\s+are\s+now\s+\w+",
        "description": "Persona hijacking - trying to reassign AI identity",
        "severity": "high"
    },
    {
        "pattern": r"pretend\s+(you\s+)?(have\s+no|don'?t\s+have)\s+(restrictions?|rules?|limits?|guidelines?)",
        "description": "Restriction bypass attempt",
        "severity": "high"
    },
    {
        "pattern": r"(system\s+prompt|your\s+instructions?|your\s+rules?).{0,30}(repeat|reveal|show|tell|print|output|display)",
        "description": "System prompt extraction attempt",
        "severity": "high"
    },
    {
        "pattern": r"(repeat|print|output|display|show).{0,30}(system\s+prompt|your\s+instructions?|above)",
        "description": "System prompt extraction - reverse phrasing",
        "severity": "high"
    },
    {
        "pattern": r"disregard\s+(all\s+)?(your\s+)?(previous|prior|above|safety|ethical)",
        "description": "Safety bypass attempt",
        "severity": "high"
    },
    {
        "pattern": r"(act|behave|respond)\s+as\s+(if\s+)?(you\s+)?(are|were|have\s+no)\s+",
        "description": "Role manipulation attempt",
        "severity": "medium"
    },
]

# THE SCANNER FUNCTION


def scan(text:str)->dict:
    """
    Scans text against all attack patterns.
    Returns a result dictionary with:
      - is_clean   : True if no attacks found, False if attack detected
      - hits       : list of patterns that matched
    """

    hits = []

    for rule in ATTACK_PATTERNS:

        match = re.search(
            rule["pattern"],
            text,
            re.IGNORECASE
        )

        if match:
            hits.append({
                "matched_text": match.group(),        # what exactly matched
                "description": rule["description"],   # what attack this is
                "severity":    rule["severity"]        # how dangerous
            })

    result = {
            "is_clean": len(hits) == 0,     # True if no hits, False if any hits
            "hits": hits
        }

    return result
