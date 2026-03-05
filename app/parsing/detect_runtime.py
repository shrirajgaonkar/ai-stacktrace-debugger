import re

def detect_runtime(log_text: str) -> str:
    if re.search(r"Traceback \(most recent call last\):", log_text):
        return "python"
    if re.search(r"    at .* \((.*:\d+:\d+)\)", log_text) or re.search(r"Error: .*\n    at ", log_text):
        return "node"
    if re.search(r"Exception in thread \".*\" ", log_text) or re.search(r"\tat .*\.java:\d+", log_text):
        return "java"
    return "generic"
