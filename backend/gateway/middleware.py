import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from backend.core.logger import logger
from backend.core.telemetry import telemetry


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time_ms = (time.time() - start_time) * 1000.0
        response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"
        
        telemetry.record_latency(f"http_{request.method}_{request.url.path}", process_time_ms)
        
        if process_time_ms > 200.0:
            logger.warning(f"[SlowRequest] {request.method} {request.url.path} took {process_time_ms:.2f}ms")
            
        return response
