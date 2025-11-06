"""Hierarchical exceptions and logging setup."""
from __future__ import annotations

import logging
from typing import Optional


logger = logging.getLogger("modern_python_demo")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class DemoError(Exception):
    """Base exception for the demo."""


class ConfigError(DemoError):
    """Configuration related errors."""


class PluginError(DemoError):
    """Plugin loading / runtime errors."""


class SerializationError(DemoError):
    """Serialization / deserialization issues."""


def log_and_raise(exc: Exception, level: str = "error") -> None:
    """Log an exception and re-raise it as DemoError if needed."""
    msg = f"{exc.__class__.__name__}: {exc}"
    if level == "warning":
        logger.warning(msg)
    else:
        logger.error(msg)
    raise exc
