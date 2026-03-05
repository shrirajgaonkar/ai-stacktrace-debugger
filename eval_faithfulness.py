import json

mock_llm_response = {
    "fixes": [
        {
            "title": "Fix division by zero",
            "steps": ["Add a sanity check to ensure denominator is not zero."],
            "code_snippets": [
                {"language": "python", "code": "if denominator != 0:\n    return numerator / denominator"}
            ],
            "risk": "low",
            "evidence": ["Based on frame #[0] in main.py", "Pattern correlation: ZeroDivisionError"]
        }
    ]
}

def evaluate_faithfulness(llm_json: dict):
    print("Evaluating LLM output faithfulness to source traces...")
    fixes = llm_json.get("fixes", [])
    
    for fix in fixes:
        evidence = fix.get("evidence", [])
        print(f"Fix Title: {fix.get('title')}")
        
        has_frame_citation = any("frame #" in e.lower() or "file:" in e.lower() for e in evidence)
        if has_frame_citation:
            print("Status: PASS - Fix cites a specific frame index or file.")
        else:
            print("Status: FAIL - Fix is lacking specific frame citations (potential hallucination).")

if __name__ == "__main__":
    evaluate_faithfulness(mock_llm_response)
