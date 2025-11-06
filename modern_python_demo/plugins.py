"""Dynamic plugin discovery and loading.

This module uses pkgutil and importlib to discover subpackages/modules under
`modern_python_demo.plugins` and loads objects that conform to a Protocol.
"""
from __future__ import annotations

import pkgutil
import importlib
from typing import List, Protocol, runtime_checkable, Any, Optional


@runtime_checkable
class PluginProtocol(Protocol):
    """Simple plugin protocol: must provide `name` and `on_event` callable."""

    name: str

    def on_event(self, event: str, payload: Any) -> None: ...


def discover_plugins(package_name: str = "modern_python_demo.plugins") -> List[PluginProtocol]:
    plugins: List[PluginProtocol] = []
    pkg = importlib.import_module(package_name)
    prefix = pkg.__name__ + "."
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, prefix):
        try:
            mod = importlib.import_module(name)
        except Exception as e:
            print(f"Failed importing plugin module {name}: {e}")
            continue
        # find plugin objects
        for attr in dir(mod):
            obj = getattr(mod, attr)
            try:
                if isinstance(obj, type) and issubclass(obj, object) and hasattr(obj, "on_event"):
                    inst = obj()
                    if isinstance(inst, PluginProtocol):
                        plugins.append(inst)
            except Exception:
                # fallback: if instance matches protocol at runtime
                try:
                    inst = obj
                    if isinstance(inst, PluginProtocol):
                        plugins.append(inst)
                except Exception:
                    continue
    return plugins
