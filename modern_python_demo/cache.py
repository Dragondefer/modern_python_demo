"""Caching utilities: lru_cache usage and custom performance decorator.
"""
from __future__ import annotations

from functools import lru_cache, wraps
import time
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])


@lru_cache(maxsize=256)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def perf(func: F) -> F:
    """Decorator that prints execution time and re-raises exceptions with context."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise
        finally:
            elapsed = time.perf_counter() - start
            print(f"[perf] {func.__name__}: {elapsed:.6f}s")

    return wrapper  # type: ignore
