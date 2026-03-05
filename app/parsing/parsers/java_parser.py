import re
from typing import List, Dict, Any

def parse(log_text: str) -> List[Dict[str, Any]]:
    frames = []
    lines = log_text.strip().split("\n")
    
    frame_regex = re.compile(r"^\s*at (.*?)\((.*?):(\d+)\)$")
    
    for line in lines:
        match = frame_regex.match(line)
        if match:
            frames.append({
                "function": match.group(1),
                "file": match.group(2),
                "line": int(match.group(3)),
                "raw_frame": line
            })
            
    return frames
