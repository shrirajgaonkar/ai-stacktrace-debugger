import re
from typing import Optional, Tuple

def find_best_match(log_text: str, patterns_from_db: list) -> Tuple[Optional[str], float]:
    """
    Given the raw log text and a list of patterns from the DB,
    returns the tuple (pattern_id, confidence_score) representing the best match.
    """
    best_match_id = None
    best_confidence = 0.0
    
    for pattern in patterns_from_db:
        regexes = pattern.regexes or []
        for reg in regexes:
            try:
                if re.search(reg, log_text):
                    # Basic exact regex match receives high confidence
                    return (str(pattern.id), 0.95)
            except re.error:
                continue
                
    return (best_match_id, best_confidence)
