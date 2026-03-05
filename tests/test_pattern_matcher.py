from app.patterns.matcher import find_best_match

class MockPattern:
    def __init__(self, id, regexes):
        self.id = id
        self.regexes = regexes

def test_find_best_match():
    patterns = [
        MockPattern(id="123", regexes=[r"ZeroDivisionError"]),
        MockPattern(id="456", regexes=[r"TypeError.*Cannot read properties"])
    ]
    
    log = "Traceback...\nZeroDivisionError: division by zero"
    match_id, conf = find_best_match(log, patterns)
    
    assert match_id == "123"
    assert conf == 0.95
