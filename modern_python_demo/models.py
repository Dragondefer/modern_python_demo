"""Data modeling: dataclasses, attrs, __slots__, descriptors, cached properties.

Demonstrates memory optimization, typed fields and custom descriptors.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Any
import attr


class NonNegative:
    """Descriptor that enforces non-negative numbers."""

    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any):
        if value is not None and value < 0:
            raise ValueError(f"{self.name} must be non-negative")
        instance.__dict__[self.name] = value


@dataclass(slots=True)
class Stats:
    """A dataclass with __slots__ for low-memory footprint."""

    count: int = 0
    total: float = 0.0

    def add(self, value: float) -> None:
        self.count += 1
        self.total += value

    @cached_property
    def mean(self) -> float:
        return (self.total / self.count) if self.count else 0.0


@attr.define(slots=True)
class AttrsPoint:
    """An attrs-based class demonstrating attrs usage and slots."""

    x: float = 0.0
    y: float = 0.0

    def distance_squared(self) -> float:
        return self.x * self.x + self.y * self.y


class Account:
    """Model using a custom descriptor for validation."""

    balance = NonNegative("balance")

    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        self.balance -= amount
