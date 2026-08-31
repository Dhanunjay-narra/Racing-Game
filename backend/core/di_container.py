from typing import Dict, Any, Type, TypeVar, Optional
from backend.core.logger import logger

T = TypeVar("T")


class Container:
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Any] = {}

    def register_singleton(self, service_type: Type[T], instance: T) -> None:
        self._services[service_type] = instance
        logger.debug(f"[Container] Registered singleton {service_type.__name__}")

    def register_factory(self, service_type: Type[T], factory: Any) -> None:
        self._factories[service_type] = factory
        logger.debug(f"[Container] Registered factory for {service_type.__name__}")

    def resolve(self, service_type: Type[T]) -> T:
        if service_type in self._services:
            return self._services[service_type]
        if service_type in self._factories:
            return self._factories[service_type]()
        raise KeyError(f"Service '{service_type.__name__}' is not registered in container.")

    def try_resolve(self, service_type: Type[T]) -> Optional[T]:
        return self._services.get(service_type) or (self._factories[service_type]() if service_type in self._factories else None)


container = Container()
