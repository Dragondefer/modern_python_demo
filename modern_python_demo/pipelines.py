"""Generator/coroutine pipelines demonstration.

Includes a decorator to turn generator functions into pipeline stages and
compose them.
"""
from __future__ import annotations

from typing import Callable, Iterator, Iterable, Any
from functools import wraps


def pipeline_stage(func: Callable[..., Iterator[Any]]) -> Callable[..., Callable[[Iterable[Any]], Iterable[Any]]]:
    """Decorator that converts a generator stage into a callable pipeline stage."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        def stage(iterable: Iterable[Any]):
            for item in func(iterable, *args, **kwargs):
                yield item

        return stage

    return wrapper


@pipeline_stage
def filter_even(items: Iterable[int]):
    for i in items:
        if i % 2 == 0:
            yield i


@pipeline_stage
def multiply(items: Iterable[int], factor: int = 2):
    for i in items:
        yield i * factor


def compose(*stages: Callable[[Iterable[Any]], Iterable[Any]]):
    def composed(data: Iterable[Any]):
        for s in stages:
            data = s(data)
        return data

    return composed
