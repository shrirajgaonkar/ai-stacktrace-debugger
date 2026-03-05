import re
from typing import List, Dict, Any

def parse(log_text: str) -> List[Dict[str, Any]]:
    frames = []
    lines = log_text.strip().split("\n")
    
    # Simple regex for python frames: File "...", line X, in Y
    frame_regex = re.compile(r"^\s*File \"(.*?)\", line (\d+), in (.*)$")
    
    current_frame = None
    
    for line in lines:
        match = frame_regex.match(line)
        if match:
            if current_frame:
                frames.append(current_frame)
            current_frame = {
                "file": match.group(1),
                "line": int(match.group(2)),
                "function": match.group(3),
                "code_line": "",
                "raw_frame": line
            }
        elif current_frame and line.startswith("    "):
            current_frame["code_line"] = line.strip()
            current_frame["raw_frame"] += "\n" + line
            frames.append(current_frame)
            current_frame = None
            
    if current_frame:
        frames.append(current_frame)
            
    return frames
