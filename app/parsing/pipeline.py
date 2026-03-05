from app.parsing.detect_runtime import detect_runtime
from app.parsing.parsers import python_parser, node_parser, java_parser, generic_parser
from typing import Dict, Any

def process_log(log_text: str) -> Dict[str, Any]:
    runtime = detect_runtime(log_text)
    
    if runtime == "python":
        frames = python_parser.parse(log_text)
    elif runtime == "node":
        frames = node_parser.parse(log_text)
    elif runtime == "java":
        frames = java_parser.parse(log_text)
    else:
        frames = generic_parser.parse(log_text)
        
    return {
        "runtime_detected": runtime,
        "parsed_frames": frames,
        "top_message": get_top_message(log_text, runtime)
    }

def get_top_message(log_text: str, runtime: str) -> str:
    lines = [l for l in log_text.split("\n") if l.strip()]
    if not lines:
        return ""
    if runtime == "python":
        # Usually the last line in a Python traceback contains the exception
        return lines[-1]
    # For Node/Java, it's typically the first line
    return lines[0]
