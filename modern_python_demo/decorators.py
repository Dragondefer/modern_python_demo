"""Advanced decorators examples: parameterized decorators, nested decorators, class-attribute decorators.

This module demonstrates:
- parameterized decorator factory
- nested decorators
- a decorator that attaches metadata to a class
- caching / timing decorators composition
"""
from __future__ import annotations

from functools import wraps, partial
from typing import Callable, Any, Optional, TypeVar, Dict
import time

F = TypeVar("F", bound=Callable[..., Any])


def timed(label: Optional[str] = None):
    """Parameterized decorator that measures execution time.

    Usage:
        @timed()
        @timed('label')
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                print(f"[timed]{label or func.__name__}: {elapsed:.6f}s")
        return wrapper  # type: ignore

    return decorator


def with_metadata(**meta):
    """Decorator that attaches metadata to a function or class as attributes.

    Shows nested decorators and attribute setting.
    """
    def deco(obj):
        for k, v in meta.items():
            setattr(obj, k, v)
        return obj

    return deco


def memoize_with_limit(maxsize: int = 128):
    """Simple LRU-ish decorator implemented with closure and dict.

    This is educational (not as robust as functools.lru_cache) and demonstrates
    closures, partials and nested decorators.
    """
    def deco(func: F) -> F:
        cache: Dict[Any, Any] = {}
        order: list = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                order.remove(key)
                order.append(key)
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            order.append(key)
            if len(order) > maxsize:
                oldest = order.pop(0)
                del cache[oldest]
            return result

        def cache_info():
            return {"size": len(cache), "maxsize": maxsize}

        wrapper.cache_info = cache_info  # type: ignore[attr-defined]
        return wrapper  # type: ignore

    return deco
