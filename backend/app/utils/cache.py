"""
Cache utilities for improving API performance.
"""
import hashlib
import json
from typing import Any, Callable, Optional
from functools import wraps

try:
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = None

from app.core.config import settings


class CacheManager:
    """Simple cache manager for API responses."""
    
    def __init__(self):
        self._cache = {}
        self.use_redis = REDIS_AVAILABLE and settings.REDIS_URL
        if self.use_redis:
            self.redis_client = Redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
        else:
            self.redis_client = None
    
    def _make_key(self, func_name: str, *args, **kwargs) -> str:
        """Create a cache key from function name and arguments."""
        key_parts = [func_name]
        
        # Add args
        for arg in args:
            if isinstance(arg, (str, int, float, bool, type(None))):
                key_parts.append(str(arg))
            else:
                key_parts.append(
                    hashlib.md5(str(arg).encode()).hexdigest()[:8]
                )
        
        # Add kwargs
        for k, v in sorted(kwargs.items()):
            if isinstance(v, (str, int, float, bool, type(None))):
                key_parts.append(f"{k}:{v}")
            else:
                key_parts.append(
                    f"{k}:{hashlib.md5(str(v).encode()).hexdigest()[:8]}"
                )
        
        return "::".join(key_parts)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if self.use_redis and self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    return json.loads(cached)
            except Exception:
                # Fall back to memory cache
                pass
        
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL (seconds)."""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.setex(key, ttl, json.dumps(value))
            except Exception:
                # Fall back to memory cache
                self._cache[key] = value
                # Simple TTL simulation for memory cache
                # In production, use proper TTL implementation
        else:
            self._cache[key] = value
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception:
                pass
        
        self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache."""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.flushdb()
            except Exception:
                pass
        
        self._cache.clear()


# Global cache instance
cache_manager = CacheManager()


def cached(ttl: int = 300):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Skip cache for certain operations
            if kwargs.get('skip_cache', False):
                return func(*args, **kwargs)
            
            # Create cache key
            key = cache_manager._make_key(
                f"{func.__module__}.{func.__name__}",
                *args,
                **{k: v for k, v in kwargs.items() if k != 'skip_cache'}
            )
            
            # Try to get from cache
            cached_result = cache_manager.get(key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def invalidate_cache(pattern: str = None):
    """
    Decorator to invalidate cache after function execution.
    
    Args:
        pattern: Pattern to match cache keys (if None, invalidates all)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if pattern:
                # In production, use Redis SCAN for pattern matching
                # For simplicity, we'll clear all cache for now
                cache_manager.clear()
            else:
                cache_manager.clear()
            
            return result
        
        return wrapper
    return decorator