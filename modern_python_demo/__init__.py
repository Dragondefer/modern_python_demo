"""modern_python_demo package

Eager-import core submodules so tooling and `__all__` work nicely for demos
and tests.
"""
"""modern_python_demo package

This package exposes a collection of modules that demonstrate modern Python
features for educational purposes. Use ``python -m modern_python_demo`` to run
the demo.
"""
from importlib.metadata import version as _version

__all__ = [
    "decorators",
    "metaclasses",
    "models",
    "events",
    "plugins",
    "cache",
    "serialization",
    "introspect",
    "pipelines",
    "config",
    "errors",
]

try:
    __version__ = _version("modern_python_demo")
except Exception:
    __version__ = "0.0.0"

# Do not import submodules eagerly; allow consumers/tests to import specific
# modules (e.g. `from modern_python_demo import cache`) or use `import
# modern_python_demo.cache` so import side-effects are minimized during test
# collection and packaging.

# Expose names but import submodules lazily to avoid import-time cycles and to
# keep package import lightweight for tooling and tests.
__all__ = [
    "decorators",
    "metaclasses",
    "models",
    "events",
    "plugins",
    "cache",
    "serialization",
    "introspect",
    "pipelines",
    "config",
    "errors",
    "__version__",
]

import importlib
from types import ModuleType
from typing import Any


def __getattr__(name: str) -> Any:
    if name in __all__:
        mod = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)
