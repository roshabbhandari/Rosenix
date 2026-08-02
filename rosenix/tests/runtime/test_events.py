import pytest

from rosenix.runtime.events import Event, EventBus


async def test_subscribed_handler_receives_event():
    bus = EventBus()
    received = []

    @bus.on("task.done")
    async def handler(event: Event) -> None:
        received.append(event.payload)

    await bus.publish(Event("task.done", {"id": 1}))
    assert received == [{"id": 1}]


async def test_sync_handler_also_works():
    bus = EventBus()
    received = []

    @bus.on("task.done")
    def handler(event: Event) -> None:
        received.append(event.payload)

    await bus.publish(Event("task.done", {"id": 2}))
    assert received == [{"id": 2}]


async def test_wildcard_handler_receives_all_events():
    bus = EventBus()
    received = []

    @bus.on(EventBus.WILDCARD)
    async def handler(event: Event) -> None:
        received.append(event.name)

    await bus.publish(Event("a"))
    await bus.publish(Event("b"))
    assert received == ["a", "b"]


async def test_unrelated_event_name_not_delivered():
    bus = EventBus()
    received = []

    @bus.on("only.this")
    async def handler(event: Event) -> None:
        received.append(event.name)

    await bus.publish(Event("something.else"))
    assert received == []


async def test_handler_exception_propagates_as_exception_group():
    bus = EventBus()

    @bus.on("boom")
    async def bad_handler(event: Event) -> None:
        raise ValueError("kaboom")

    with pytest.raises(ExceptionGroup):
        await bus.publish(Event("boom"))


async def test_unsubscribe_stops_delivery():
    bus = EventBus()
    received = []

    async def handler(event: Event) -> None:
        received.append(event.name)

    bus.subscribe("x", handler)
    bus.unsubscribe("x", handler)
    await bus.publish(Event("x"))
    assert received == []
