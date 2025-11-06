import asyncio
import importlib

# Import submodules via importlib to avoid relying on eager package attributes
cache = importlib.import_module("modern_python_demo.cache")
serialization = importlib.import_module("modern_python_demo.serialization")
pipelines = importlib.import_module("modern_python_demo.pipelines")
introspect = importlib.import_module("modern_python_demo.introspect")
from modern_python_demo.events import EventBroker
from modern_python_demo.decorators import memoize_with_limit


def test_fib_basic():
    assert cache.fib(0) == 0
    assert cache.fib(1) == 1
    assert cache.fib(5) == 5


def test_serialization_json_roundtrip():
    obj = {"a": 1, "b": "x"}
    s = serialization.dumps_json(obj)
    r = serialization.loads_json(s)
    assert r["data"]["a"] == 1


def test_pipeline_compose():
    pipeline = pipelines.compose(pipelines.filter_even(), pipelines.multiply(factor=3))
    data = list(pipeline(range(6)))
    # filter_even yields 0,2,4; multiply by 3 -> 0,6,12
    assert data == [0, 6, 12]


def test_introspect_factory():
    f = introspect.factory_from_spec("test", multiplier=4)
    assert f(2) == 8


def test_eventbroker_emit():
    async def run_emit():
        broker = EventBroker()
        results = []

        def h(event, payload):
            results.append((event, payload))

        async def ah(event, payload):
            results.append(("async:" + event, payload))

        broker.subscribe("e", h)
        broker.subscribe("e", ah)
        await broker.emit("e", {"x": 1})
        return results

    res = asyncio.run(run_emit())
    # handlers append two items
    assert any(r[0] == "e" for r in res)
    assert any(r[0].startswith("async:") for r in res)


def test_memoize_decorator():
    @memoize_with_limit(2)
    def add(a, b=0):
        return a + b

    assert add(1, 2) == 3
    assert add(1, b=2) == 3
