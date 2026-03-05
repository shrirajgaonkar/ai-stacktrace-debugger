# Minimal rate limiting (in-memory)
# Note: For production, this should use Redis. 
from fastapi import HTTPException, Request
from collections import defaultdict
import time

class SimpleRateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.history = defaultdict(list)
        
    def check_rate_limit(self, key: str):
        now = time.time()
        # Clean old entries
        self.history[key] = [t for t in self.history[key] if now - t < self.period]
        
        if len(self.history[key]) >= self.calls:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
        self.history[key].append(now)

# Usage example:
# limiter = SimpleRateLimiter(calls=10, period=60)
# limiter.check_rate_limit(user.id)
