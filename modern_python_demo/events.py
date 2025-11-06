"""Async event broker, observer pattern, scheduling and tasks.

Provides:
- EventBroker: subscribe / unsubscribe / emit (sync and async handlers)
- Scheduler: simple asyncio-based scheduled tasks
"""
from __future__ import annotations

import asyncio
from typing import Callable, Any, Awaitable, Dict, List, Optional
from functools import partial

Handler = Callable[..., Any]
AsyncHandler = Callable[..., Awaitable[Any]]


class EventBroker:
    """A simple pub/sub broker mixing sync and async handlers.

    Handlers can be regular callables or async callables. Emission will await
    async handlers and call sync handlers in the event loop's default executor.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Handler]] = {}

    def subscribe(self, event: str, handler: Handler) -> None:
        self._subscribers.setdefault(event, []).append(handler)

    def unsubscribe(self, event: str, handler: Handler) -> None:
        handlers = self._subscribers.get(event)
        if handlers and handler in handlers:
            handlers.remove(handler)

    async def emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event to all subscribers.

        Handlers receive the event name as the first argument, followed by
        whatever payload was passed to emit. Supports both async and sync
        handlers (sync handlers are executed in the default executor).
        """
        handlers = list(self._subscribers.get(event, []))
        tasks = []
        for h in handlers:
            if asyncio.iscoroutinefunction(h):
                # pass event name first
                tasks.append(h(event, *args, **kwargs))
            else:
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, partial(h, event, *args, **kwargs)))
        if tasks:
            await asyncio.gather(*tasks)


class Scheduler:
    """A small scheduler to run periodic tasks via asyncio.

    It supports starting and stopping tasks and scheduling one-off delayed calls.
    """

    def __init__(self) -> None:
        self._tasks: List[asyncio.Task] = []

    def schedule_periodic(self, coro_func: AsyncHandler, interval: float) -> asyncio.Task:
        async def runner():
            while True:
                try:
                    await coro_func()
                except Exception as e:
                    print(f"Scheduler task error: {e}")
                await asyncio.sleep(interval)

        task = asyncio.create_task(runner())
        self._tasks.append(task)
        return task

    def schedule_once(self, delay: float, coro_func: AsyncHandler) -> asyncio.Task:
        async def runner():
            await asyncio.sleep(delay)
            await coro_func()

        task = asyncio.create_task(runner())
        self._tasks.append(task)
        return task

    def cancel_all(self) -> None:
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()
