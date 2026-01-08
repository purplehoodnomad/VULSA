from collections import defaultdict
from typing import Callable, Type


class EventBus:
    def __init__(self):
        self._handlers: dict[Type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, events: list) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                await handler(event)
