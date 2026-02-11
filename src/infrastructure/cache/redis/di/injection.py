from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from container import Container

from domain.link.cache import AbstractLinkCache
from infrastructure.cache.redis.client import RedisClient


@inject
def get_link_cache(client: RedisClient = Depends(Provide[Container.redis_client])) -> AbstractLinkCache:
    return Container.link_cache_factory(client=client.client)