import asyncio
from app.patterns.seed_patterns import SEED_PATTERNS
from app.patterns.matcher import find_best_match

class MockPattern:
    def __init__(self, d):
        self.id = d["name"]
        self.regexes = d["regexes"]

patterns_db = [MockPattern(p) for p in SEED_PATTERNS]

sample_logs = [
    """Traceback (most recent call last):
  File "main.py", line 10, in <module>
    x = 1 / 0
ZeroDivisionError: division by zero""",
    
    """TypeError: Cannot read properties of undefined (reading 'map')
    at renderList (app.js:45:12)"""
]

def run_eval():
    print("Running Pattern matching evaluation...\n")
    for log in sample_logs:
        match_id, conf = find_best_match(log, patterns_db)
        print("Log Excerpt:")
        print(log.strip())
        if match_id:
            print(f"-> Matched Pattern ID: {match_id} (Confidence: {conf})")
        else:
            print("-> No match found.")
        print("-" * 40)

if __name__ == "__main__":
    run_eval()
