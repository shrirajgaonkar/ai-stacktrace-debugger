import os
from typing import Dict, Any

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")

def load_prompt(filename: str) -> str:
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

EXPLAIN_SYSTEM_V1 = load_prompt("explain_v1.txt")
ROOT_CAUSE_SYSTEM_V1 = load_prompt("rootcause_json_v1.txt")
FIX_STEPS_SYSTEM_V1 = load_prompt("fixsteps_json_v1.txt")

def build_user_prompt(raw_log: str, parsed_frames: list, pattern_context: str = None) -> str:
    prompt = f"Raw Log:\n```\n{raw_log}\n```\n\nParsed Frames:\n"
    for i, frame in enumerate(parsed_frames):
        prompt += f"[{i}] {frame.get('file', 'Unknown')}:{frame.get('line', '?')} in {frame.get('function', 'Unknown')}\n"
        
    if pattern_context:
        prompt += f"\nPattern Match Context:\n{pattern_context}\n"
        
    return prompt
