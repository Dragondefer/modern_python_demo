"""Introspection utilities using inspect and typing to dynamically build functions.

Demonstrates: inspect.signature, annotations, closures, partials and dynamic factory.
"""
from __future__ import annotations

import inspect
from functools import partial
from typing import Callable, Any


def summarize_callable(func: Callable[..., Any]) -> dict:
    sig = inspect.signature(func)
    return {
        "name": getattr(func, "__name__", repr(func)),
        "params": [p.name for p in sig.parameters.values()],
        "return": sig.return_annotation,
    }


def make_adder(x: int) -> Callable[[int], int]:
    """Dynamically create and return a closure that adds x."""
    def add(y: int) -> int:
        return x + y

    return add


def factory_from_spec(name: str, *, multiplier: int = 1) -> Callable[[int], int]:
    """Return a function built dynamically with partials and closures."""
    def base(a: int) -> int:
        return a * multiplier

    base.__name__ = name
    return base
