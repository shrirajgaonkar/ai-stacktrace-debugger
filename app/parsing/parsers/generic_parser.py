from typing import List, Dict, Any

def parse(log_text: str) -> List[Dict[str, Any]]:
    return [{"raw_frame": line} for line in log_text.split("\n") if line.strip()]
