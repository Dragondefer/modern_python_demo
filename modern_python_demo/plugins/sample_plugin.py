"""A small sample plugin demonstrating the PluginProtocol."""

from __future__ import annotations

from typing import Any


class SamplePlugin:
    name = "sample"

    def on_event(self, event: str, payload: Any) -> None:
        print(f"[SamplePlugin] Event {event} -> payload={payload}")


# Also expose a function-based plugin-like object

def simple_on_event(event: str, payload: Any) -> None:
    print(f"[sample_func] {event}: {payload}")

# Provide an instance
plugin_instance = SamplePlugin()
