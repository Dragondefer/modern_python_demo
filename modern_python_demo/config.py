"""Configuration system: dataclass-based config, YAML loading, context manager for temporary overrides."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Iterator, Optional, ContextManager
from contextlib import contextmanager

try:
    import yaml
except Exception:
    yaml = None


@dataclass(frozen=True)
class Config:
    app_name: str = "ModernDemo"
    debug: bool = False
    interval: float = 1.0
    plugin_enabled: bool = True

    def with_override(self, **kwargs) -> "Config":
        return replace(self, **kwargs)


@contextmanager
def temp_config(cfg: Config, **overrides) -> Iterator[Config]:
    """Temporarily yield an overridden config inside a context manager."""
    new = cfg.with_override(**overrides)
    try:
        yield new
    finally:
        pass


def load_from_yaml(path: str) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML not installed")
    with open(path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)
