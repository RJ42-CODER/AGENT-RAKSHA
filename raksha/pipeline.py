from raksha.ingress.normalizer import clean
from raksha.ingress.regex_rules import scan as regex_scan
from raksha.ingress.semantic import analyze

def scan(text: str) -> str:
    """
    Master pipeline - runs all 3 gates in order.
    Returns final verdict with trust score.
    """

    #GATE1A : clean text
    cleaned_text = clean(text)

    #GATE1B : Regex scan
    regex_result = regex_scan(cleaned_text)

    if not regex_result["is_clean"]:
        return{ 
            "blocked": True,
            "trust_score":0,
            "gate":"regex",
            "reason": regex_result["hits"][0]["description"],
            "severity": regex_result["hits"][0]["severity"],
            "hits": regex_result["hits"]
        }
    
    #GATE1C: Semantic scan(only if regex passed)
    semantic_result = analyze(cleaned_text)

    if not semantic_result["is_clean"]:
        return {
            "blocked": True,
            "trust_score": 30,
            "gate": "semantic",
            "reason": semantic_result["reason"],
            "severity": "high",
            "hits": []
        }
    
    #ALL CLEAR
    return{
        "blocked": False,
        "trust_score": 100,
        "gate": None,
        "reason": "All checks passed",
        "severity": None,
        "hits": []
    }