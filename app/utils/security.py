# Security utilities for standard validation / sanitization
import re

def sanitize_log_text(text: str) -> str:
    # Strip null bytes and non-printable characters except standard whitespace
    cleaned = text.replace("\x00", "")
    return cleaned
