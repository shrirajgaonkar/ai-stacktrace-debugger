import re
from typing import List, Dict, Any

def parse(log_text: str) -> List[Dict[str, Any]]:
    frames = []
    lines = log_text.strip().split("\n")
    
    frame_regex = re.compile(r"^\s*at (.*?) \((.*?):(\d+):(\d+)\)$")
    frame_regex_alt = re.compile(r"^\s*at (.*?):(\d+):(\d+)$")
    
    for line in lines:
        match = frame_regex.match(line)
        if match:
            frames.append({
                "function": match.group(1),
                "file": match.group(2),
                "line": int(match.group(3)),
                "raw_frame": line
            })
            continue
            
        match_alt = frame_regex_alt.match(line)
        if match_alt:
            frames.append({
                "function": "<anonymous>",
                "file": match_alt.group(1),
                "line": int(match_alt.group(2)),
                "raw_frame": line
            })
            
    return frames
