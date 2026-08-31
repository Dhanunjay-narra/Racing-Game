import time
from collections import defaultdict
from fastapi import Request, HTTPException, status


class InMemoryRateLimiter:
    def __init__(self, requests_per_minute: int = 120):
        self.rpm = requests_per_minute
        self.requests = defaultdict(list)

    async def check(self, request: Request):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        minute_ago = now - 60.0
        
        self.requests[client_ip] = [t for t in self.requests[client_ip] if t > minute_ago]
        
        if len(self.requests[client_ip]) >= self.rpm:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please throttle your requests."
            )
            
        self.requests[client_ip].append(now)


rate_limiter = InMemoryRateLimiter()
