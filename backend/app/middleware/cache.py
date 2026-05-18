"""
Simple caching middleware for API responses
"""
from fastapi import Request, Response
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """
    In-memory cache for API responses
    For production, use Redis or Memcached
    """
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, Tuple[str, datetime]] = {}
        self.default_ttl = default_ttl  # 5 minutes default
    
    def _generate_key(self, request: Request) -> str:
        """Generate cache key from request"""
        # Include method, path, and query params
        key_parts = [
            request.method,
            request.url.path,
            str(sorted(request.query_params.items()))
        ]
        
        # Include user ID if authenticated
        if hasattr(request.state, 'user_id'):
            key_parts.append(f"user:{request.state.user_id}")
        
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, request: Request) -> Optional[str]:
        """Get cached response if available and not expired"""
        key = self._generate_key(request)
        
        if key in self.cache:
            content, expires_at = self.cache[key]
            
            # Check if expired
            if datetime.now() < expires_at:
                logger.debug(f"Cache hit for {request.url.path}")
                return content
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache expired for {request.url.path}")
        
        logger.debug(f"Cache miss for {request.url.path}")
        return None
    
    def set(self, request: Request, content: str, ttl: Optional[int] = None):
        """Cache response content"""
        key = self._generate_key(request)
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = (content, expires_at)
        logger.debug(f"Cached response for {request.url.path} (TTL: {ttl}s)")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def clear_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, (_, expires_at) in self.cache.items()
            if now >= expires_at
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleared {len(expired_keys)} expired cache entries")


# Global cache instance
cache = SimpleCache(default_ttl=300)


def should_cache(request: Request) -> bool:
    """Determine if request should be cached"""
    # Only cache GET requests
    if request.method != "GET":
        return False
    
    # Don't cache health checks
    if request.url.path in ["/", "/health"]:
        return False
    
    # Cache statistics and history
    cacheable_paths = ["/api/statistics", "/api/history"]
    return any(request.url.path.startswith(path) for path in cacheable_paths)


async def cache_middleware(request: Request, call_next):
    """
    Middleware to cache GET requests
    """
    # Check if should cache
    if not should_cache(request):
        return await call_next(request)
    
    # Try to get from cache
    cached_content = cache.get(request)
    if cached_content:
        return Response(
            content=cached_content,
            media_type="application/json",
            headers={
                "X-Cache": "HIT",
                "X-Cache-TTL": str(cache.default_ttl)
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Cache successful responses
    if response.status_code == 200:
        # Read response body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        
        # Cache the response
        cache.set(request, body.decode())
        
        # Return new response with body
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    
    return response
