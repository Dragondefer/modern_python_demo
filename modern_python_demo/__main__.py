"""Module entrypoint so the package can be run with `python -m modern_python_demo`."""
from __future__ import annotations

from .main import main
import asyncio


def _run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    _run()
