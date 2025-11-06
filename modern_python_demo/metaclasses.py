"""Metaclass and class hooks demonstration.

Includes:
- Registry metaclass that collects subclasses
- Base class with __init_subclass__ hook demonstration
"""
from __future__ import annotations

from typing import Dict, Type, Any


class RegistryMeta(type):
    """A metaclass that registers classes into a central registry.

    It shows how metaclasses can modify class creation and attach attributes.
    """
    _registry: Dict[str, Type[Any]] = {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace)
        # attach a marker attribute
        setattr(cls, "_registered_by", mcls.__name__)
        if name != "RegisteredBase":
            mcls._registry[f"{cls.__module__}.{name}"] = cls
        return cls

    @classmethod
    def get_registry(mcls) -> Dict[str, Type[Any]]:
        return dict(mcls._registry)


class RegisteredBase(metaclass=RegistryMeta):
    """Base class that also demonstrates __init_subclass__ hook.

    Subclasses will be auto-registered by the metaclass and can also perform
    custom initialization via __init_subclass__.
    """

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        # Example hook: attach a versioned attribute
        if not hasattr(cls, "version"):
            cls.version = "0.1"
