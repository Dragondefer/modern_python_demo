"""Protocols, ABCs and Generic examples for pedagogical purposes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Generic, TypeVar

T = TypeVar("T")


class Service(ABC, Generic[T]):
    """Abstract base generic service defining a contract."""

    @abstractmethod
    def process(self, item: T) -> T:
        ...


@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...


class UpperService(Service[str]):
    def process(self, item: str) -> str:
        return item.upper()