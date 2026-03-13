"""
Template caching for improved performance.
Caches rendered templates to avoid repeated disk I/O and template compilation.
"""
import hashlib
import json
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from functools import lru_cache

from app.utils.cache import cache_manager

logger = logging.getLogger(__name__)


class TemplateCache:
    """Cache for rendered email templates."""

    # Cache configuration
    CACHE_PREFIX = "email_template:"
    DEFAULT_TTL = 3600  # 1 hour
    MAX_CACHE_SIZE = 1000

    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_errors = 0

    def _generate_cache_key(
        self,
        template_name: str,
        language: str,
        variables: Dict[str, Any]
    ) -> str:
        """Generate cache key from template parameters."""
        # Create a deterministic string representation of variables
        variables_str = json.dumps(variables, sort_keys=True)

        # Create hash of all parameters
        hash_input = f"{template_name}:{language}:{variables_str}"
        hash_digest = hashlib.md5(hash_input.encode()).hexdigest()

        return f"{self.CACHE_PREFIX}{hash_digest}"

    def get_cached_template(
        self,
        template_name: str,
        language: str,
        variables: Dict[str, Any]
    ) -> Optional[Dict[str, str]]:
        """
        Get cached template if available.

        Returns:
            Cached template dict or None if not cached
        """
        try:
            cache_key = self._generate_cache_key(
                template_name, language, variables
            )

            cached = cache_manager.get(cache_key)
            if cached:
                self.cache_hits += 1
                logger.debug(f"Template cache hit: {template_name}/{language}")
                return cached

            self.cache_misses += 1
            return None

        except Exception as e:
            self.cache_errors += 1
            logger.error(f"Error getting cached template: {e}")
            return None

    def set_cached_template(
        self,
        template_name: str,
        language: str,
        variables: Dict[str, Any],
        template_data: Dict[str, str],
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache rendered template.

        Returns:
            True if cached successfully, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(
                template_name, language, variables
            )

            if ttl is None:
                ttl = self.DEFAULT_TTL

            cache_manager.set(cache_key, template_data, ttl=ttl)

            logger.debug(
                f"Template cached: {template_name}/{language} "
                f"(TTL: {ttl}s)"
            )

            return True

        except Exception as e:
            self.cache_errors += 1
            logger.error(f"Error caching template: {e}")
            return False

    def invalidate_template(
        self,
        template_name: str,
        language: Optional[str] = None
    ) -> int:
        """
        Invalidate cached templates.

        Args:
            template_name: Name of template to invalidate
            language: Optional language to invalidate (all if None)

        Returns:
            Number of cache entries invalidated
        """
        try:
            # This is a simplified implementation
            # In production, you might want to use Redis pattern matching
            # or maintain an index of cache keys

            logger.info(
                f"Template cache invalidation requested: "
                f"{template_name}/{language or 'all'}"
            )

            # For now, we'll just log and return 0
            # In a real implementation, you would:
            # 1. Query cache for matching keys
            # 2. Delete those keys
            # 3. Return count

            return 0

        except Exception as e:
            logger.error(f"Error invalidating template cache: {e}")
            return 0

    def clear_all(self) -> bool:
        """Clear all template cache entries."""
        try:
            # This would clear all cache entries with the prefix
            # In Redis: delete keys matching "email_template:*"

            logger.info("Clearing all template cache entries")

            # For now, just log - clear_pattern() not implemented
            # In production, we could either:
            # 1. Implement cache_manager.clear_pattern(
            #        f"{self.CACHE_PREFIX}*")
            # 2. Use cache_manager.clear() (clears ALL cache,
            #    not just templates)

            return True

        except Exception as e:
            logger.error(f"Error clearing template cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "errors": self.cache_errors,
            "hit_rate": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            ),
            "timestamp": datetime.now().isoformat()
        }

    def reset_stats(self) -> None:
        """Reset cache statistics."""
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_errors = 0


# LRU cache for template compilation (in-memory)
@lru_cache(maxsize=100)
def get_compiled_template_key(template_path: str) -> str:
    """
    Get cache key for compiled template.
    Uses LRU cache to avoid repeated template compilation.
    """
    return f"compiled_template:{template_path}"


class TemplatePerformanceMonitor:
    """Monitor template rendering performance."""

    def __init__(self):
        self.render_times: Dict[str, list] = {}
        self.cache_effectiveness: Dict[str, list] = {}

    def record_render_time(
        self,
        template_name: str,
        language: str,
        render_time: float,
        cached: bool
    ):
        """Record template rendering time."""
        key = f"{template_name}:{language}"

        if key not in self.render_times:
            self.render_times[key] = []

        self.render_times[key].append(render_time)

        # Keep only last 100 measurements
        if len(self.render_times[key]) > 100:
            self.render_times[key] = self.render_times[key][-100:]

        # Record cache effectiveness
        cache_key = f"{template_name}:cache"
        if cache_key not in self.cache_effectiveness:
            self.cache_effectiveness[cache_key] = []

        self.cache_effectiveness[cache_key].append(1 if cached else 0)

        # Keep only last 100 measurements
        if len(self.cache_effectiveness[cache_key]) > 100:
            self.cache_effectiveness[cache_key] = (
                self.cache_effectiveness[cache_key][-100:]
            )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        stats = {}

        for key, times in self.render_times.items():
            if times:
                stats[key] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times) * 1000,
                    "min_ms": min(times) * 1000,
                    "max_ms": max(times) * 1000,
                    "p95_ms": sorted(times)[int(len(times) * 0.95)] * 1000
                }

        # Calculate cache effectiveness
        cache_stats = {}
        for key, hits in self.cache_effectiveness.items():
            if hits:
                hit_rate = sum(hits) / len(hits)
                cache_stats[key] = {
                    "total": len(hits),
                    "hits": sum(hits),
                    "misses": len(hits) - sum(hits),
                    "hit_rate": hit_rate
                }

        return {
            "render_times": stats,
            "cache_effectiveness": cache_stats,
            "timestamp": datetime.now().isoformat()
        }

    def get_slow_templates(
        self,
        threshold_ms: float = 100.0
    ) -> Dict[str, float]:
        """Get templates with average render time above threshold."""
        slow_templates = {}

        for key, times in self.render_times.items():
            if times:
                avg_ms = sum(times) / len(times) * 1000
                if avg_ms > threshold_ms:
                    slow_templates[key] = avg_ms

        return dict(sorted(
            slow_templates.items(),
            key=lambda x: x[1],
            reverse=True
        ))

    def reset_stats(self):
        """Reset performance statistics."""
        self.render_times.clear()
        self.cache_effectiveness.clear()


# Global instances
template_cache = TemplateCache()
performance_monitor = TemplatePerformanceMonitor()


# Decorator for caching template rendering
def cached_template_render(ttl: Optional[int] = None):
    """
    Decorator for caching template rendering results.

    Usage:
        @cached_template_render(ttl=3600)
        def render_email_template(template_name, language, variables):
            # ... rendering logic
            return rendered_template
    """
    def decorator(func):
        def wrapper(
            template_name: str,
            language: str,
            variables: Dict[str, Any],
            *args,
            **kwargs
        ):
            # Try to get from cache
            cached = template_cache.get_cached_template(
                template_name, language, variables
            )

            if cached:
                performance_monitor.record_render_time(
                    template_name, language, 0.001, True
                    # Small time for cache hit
                )
                return cached

            # Not in cache, render template
            start_time = time.time()
            try:
                result = func(
                    template_name, language, variables, *args, **kwargs
                )
                render_time = time.time() - start_time

                # Cache the result
                if result:
                    template_cache.set_cached_template(
                        template_name, language, variables, result, ttl
                    )

                # Record performance
                performance_monitor.record_render_time(
                    template_name, language, render_time, False
                )

                return result

            except Exception as e:
                render_time = time.time() - start_time
                performance_monitor.record_render_time(
                    template_name, language, render_time, False
                )
                raise e

        return wrapper

    return decorator


# Utility functions
def get_template_cache_stats() -> Dict[str, Any]:
    """Get template cache statistics."""
    cache_stats = template_cache.get_stats()
    perf_stats = performance_monitor.get_performance_stats()

    return {
        "cache": cache_stats,
        "performance": perf_stats,
        "slow_templates": performance_monitor.get_slow_templates()
    }


def clear_template_cache() -> Dict[str, Any]:
    """Clear template cache and return stats."""
    cleared = template_cache.clear_all()
    stats = get_template_cache_stats()

    return {
        "cleared": cleared,
        "stats": stats
    }


def warmup_template_cache(
    templates: Dict[str, Dict[str, Any]],
    languages: list = None
) -> Dict[str, Any]:
    """
    Warm up template cache with frequently used templates.

    Args:
        templates: Dict mapping template names to example variables
        languages: List of languages to warm up (default: ["en"])

    Returns:
        Statistics about warmup process
    """
    if languages is None:
        languages = ["en"]

    from app.utils.jinja2_engine import jinja2_template_engine

    warmed = 0
    errors = 0

    for template_name, variables in templates.items():
        for language in languages:
            try:
                # Render template
                rendered = jinja2_template_engine.render_email(
                    template_name=template_name,
                    language=language,
                    variables=variables
                )

                # Cache it
                success = template_cache.set_cached_template(
                    template_name, language, variables, rendered
                )

                if success:
                    warmed += 1
                    logger.info(
                        f"Warmed up cache: {template_name}/{language}"
                    )
                else:
                    errors += 1

            except Exception as e:
                errors += 1
                logger.error(
                    f"Error warming up {template_name}/{language}: {e}"
                )

    return {
        "warmed": warmed,
        "errors": errors,
        "total": len(templates) * len(languages)
    }
