"""Demo orchestrator bringing all pieces together.

Run this module to see the features in action.
"""
from __future__ import annotations

import asyncio
import time
from typing import Any

from .config import Config, temp_config
from .decorators import timed, memoize_with_limit, with_metadata
from .metaclasses import RegisteredBase, RegistryMeta
from .models import Stats, AttrsPoint, Account
from .events import EventBroker, Scheduler
from .plugin_loader import discover_plugins
from .serialization import dumps_json, loads_json, dumps_pickle, loads_pickle
from .cache import fib, perf
from .introspect import summarize_callable, make_adder, factory_from_spec
from .pipelines import filter_even, multiply, compose
from .errors import logger


@with_metadata(author="demo", created=time.time())
class DemoTask(RegisteredBase):
    """A demo task class that will be auto-registered by the metaclass."""

    def __init__(self, name: str):
        self.name = name

    async def run(self, broker: EventBroker) -> None:
        await broker.emit("task.started", {"name": self.name})
        await asyncio.sleep(0.1)
        await broker.emit("task.finished", {"name": self.name})


async def main() -> None:
    cfg = Config()
    logger.info(f"Starting demo (debug={cfg.debug})")

    # Event system demo
    broker = EventBroker()

    def on_started(event: str, payload: Any) -> None:
        print(f"[on_started] {event}: {payload}")

    async def on_finished(event: str, payload: Any) -> None:
        print(f"[on_finished] {event}: {payload}")

    broker.subscribe("task.started", on_started)
    broker.subscribe("task.finished", on_finished)

    # Scheduler demo
    scheduler = Scheduler()

    async def periodic():
        print("[scheduler] periodic tick")

    periodic_task = scheduler.schedule_periodic(periodic, cfg.interval)

    # Plugins
    plugins = discover_plugins()
    print("Discovered plugins:", [p.name for p in plugins if hasattr(p, 'name')])
    for p in plugins:
        try:
            p.on_event("init", {"cfg": vars(cfg)})
        except Exception as e:
            print("Plugin error:", e)

    # Models and caching
    stats = Stats()
    stats.add(10)
    stats.add(20)
    print("mean:", stats.mean)

    p = AttrsPoint(3, 4)
    print("distance^2:", p.distance_squared())

    a = Account("Alice", 100.0)
    a.deposit(50.0)
    try:
        a.withdraw(300.0)
    except Exception as e:
        print("Withdraw error (expected):", e)

    # caching
    print("fib(20):", fib(20))

    # introspection and dynamic functions
    adder = make_adder(5)
    print("adder(10):", adder(10))
    mult = factory_from_spec("mul3", multiplier=3)
    print("mult(7):", mult(7))
    print("summarize mult:", summarize_callable(mult))

    # pipelines
    pipeline = compose(filter_even(), multiply(factor=3))
    data = list(pipeline(range(10)))
    print("pipeline result:", data)

    # decorators
    @timed("heavy")
    @memoize_with_limit(10)
    def heavy(n: int) -> int:
        total = 0
        for i in range(n):
            total += i
        return total

    print("heavy(100000):", heavy(100000))
    print("heavy cache info:", getattr(heavy, "cache_info", lambda: None)())

    # serialization
    payload = {"stats": {"mean": stats.mean}}
    s = dumps_json(payload)
    print("json dump:", s)
    print("json load:", loads_json(s))

    pkl = dumps_pickle(payload)
    print("pickle load:", loads_pickle(pkl))

    # metaclass registry
    print("Registered classes:", RegistryMeta.get_registry())

    # temporary config
    with temp_config(cfg, debug=True) as tcfg:
        print("temp config debug:", tcfg.debug)

    # short run to let scheduler tick and tasks operate
    tasks = [asyncio.create_task(DemoTask("t1").run(broker)), asyncio.create_task(DemoTask("t2").run(broker))]
    await asyncio.gather(*tasks)

    # cancel scheduler and finish
    scheduler.cancel_all()
    print("Demo complete")


if __name__ == "__main__":
    asyncio.run(main())
