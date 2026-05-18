"""
Rate limiting middleware for API protection
"""
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use Redis or similar
    """
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Try to get user ID from auth
        if hasattr(request.state, 'user_id'):
            return f"user:{request.state.user_id}"
        
        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0]}"
        
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"
    
    def _clean_old_requests(self, client_id: str):
        """Remove requests older than 1 minute"""
        cutoff = datetime.now() - timedelta(minutes=1)
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]
    
    async def check_rate_limit(self, request: Request) -> Tuple[bool, int, int]:
        """
        Check if request is within rate limit
        
        Returns:
            (is_allowed, remaining_requests, reset_time_seconds)
        """
        client_id = self._get_client_id(request)
        
        # Clean old requests
        self._clean_old_requests(client_id)
        
        # Count current requests
        current_requests = len(self.requests[client_id])
        
        # Check if limit exceeded
        if current_requests >= self.requests_per_minute:
            # Calculate reset time
            oldest_request = min(self.requests[client_id])
            reset_time = int((oldest_request + timedelta(minutes=1) - datetime.now()).total_seconds())
            
            return False, 0, max(reset_time, 0)
        
        # Add current request
        self.requests[client_id].append(datetime.now())
        
        # Calculate remaining
        remaining = self.requests_per_minute - (current_requests + 1)
        
        return True, remaining, 60


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to enforce rate limiting
    """
    # Skip rate limiting for health checks
    if request.url.path in ["/", "/health"]:
        return await call_next(request)
    
    # Check rate limit
    is_allowed, remaining, reset_time = await rate_limiter.check_rate_limit(request)
    
    if not is_allowed:
        logger.warning(f"Rate limit exceeded for {rate_limiter._get_client_id(request)}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please try again in {reset_time} seconds.",
                "retry_after": reset_time
            },
            headers={
                "Retry-After": str(reset_time),
                "X-RateLimit-Limit": str(rate_limiter.requests_per_minute),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_time)
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_time)
    
    return response
