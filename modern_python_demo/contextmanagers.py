"""Custom context managers examples: class-based and generator-based."""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


class Timer:
    """Class-based context manager that measures elapsed time."""

    def __init__(self, name: str = "block") -> None:
        self.name = name
        self.start: float | None = None
        self.elapsed: float | None = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - (self.start or 0.0)
        print(f"[Timer:{self.name}] {self.elapsed:.6f}s")
        return False


@contextmanager
def temp_resource(x: int) -> Iterator[int]:
    """A tiny generator-based context manager that yields a manipulated value."""
    try:
        yield x * 2
    finally:
        pass
