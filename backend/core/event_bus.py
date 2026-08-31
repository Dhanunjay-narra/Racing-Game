import asyncio
from typing import Dict, List, Callable, Any, Awaitable
from collections import defaultdict
from backend.core.logger import logger


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = defaultdict(list)
        self._sync_subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self._event_history: List[Dict[str, Any]] = []
        self._max_history = 1000

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        self._subscribers[event_type].append(handler)
        logger.debug(f"[EventBus] Subscribed async handler to '{event_type}'")

    def subscribe_sync(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        self._sync_subscribers[event_type].append(handler)
        logger.debug(f"[EventBus] Subscribed sync handler to '{event_type}'")

    async def publish(self, event_type: str, data: Dict[str, Any]):
        event_payload = {
            "event_type": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        self._event_history.append(event_payload)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

        for sync_handler in self._sync_subscribers.get(event_type, []):
            try:
                sync_handler(data)
            except Exception as e:
                logger.error(f"[EventBus] Error in sync handler for '{event_type}': {e}")

        async_handlers = self._subscribers.get(event_type, [])
        if async_handlers:
            tasks = [asyncio.create_task(h(data)) for h in async_handlers]
            await asyncio.gather(*tasks, return_exceptions=True)

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._event_history[-limit:]


event_bus = EventBus()
