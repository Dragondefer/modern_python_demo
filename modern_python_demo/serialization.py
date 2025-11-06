"""Serialization utilities with versioning: JSON, pickle, YAML.

This module demonstrates adding a version field and safe loading.
"""
from __future__ import annotations

import json
import pickle
from typing import Any, Dict

try:
    import yaml
except Exception:
    yaml = None  # optional dependency


CURRENT_VERSION = "1.0"


def dumps_json(obj: Any, *, version: str = CURRENT_VERSION) -> str:
    payload = {"__version__": version, "data": obj}
    return json.dumps(payload, default=lambda o: getattr(o, "__dict__", str(o)))


def loads_json(s: str) -> Dict[str, Any]:
    payload = json.loads(s)
    version = payload.get("__version__")
    data = payload.get("data")
    return {"version": version, "data": data}


def dumps_pickle(obj: Any) -> bytes:
    return pickle.dumps({"__version__": CURRENT_VERSION, "data": obj})


def loads_pickle(b: bytes) -> Dict[str, Any]:
    payload = pickle.loads(b)
    return {"version": payload.get("__version__"), "data": payload.get("data")}


def dumps_yaml(obj: Any) -> str:
    if yaml is None:
        raise RuntimeError("PyYAML not installed")
    return yaml.safe_dump({"__version__": CURRENT_VERSION, "data": obj})


def loads_yaml(s: str) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML not installed")
    payload = yaml.safe_load(s)
    return {"version": payload.get("__version__"), "data": payload.get("data")}
