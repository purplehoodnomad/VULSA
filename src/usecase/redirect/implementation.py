from infrastructure.uow.link import AbstractLinkUnitOfWork
from domain.value_objects.link import Short

from domain.link.cache import AbstractLinkCache
from infrastructure.cache.entries.link import LinkCacheEntry
from infrastructure.cache.exceptions import CacheMiss
from usecase.link.utils.dto import SimpleLinkDTO

from .abstract import AbstractLinkRedirectUseCase


class LinkRedirectUseCase(AbstractLinkRedirectUseCase):
    def __init__(
        self,
        uow: AbstractLinkUnitOfWork,
        link_cache: AbstractLinkCache
    ):
        self.uow = uow
        self.link_cache = link_cache

    async def execute(
        self,
        short: str,
    ) -> SimpleLinkDTO:
        # trying to get from cache
        try:
            entry = await self.link_cache.get_and_increment(short)
            return SimpleLinkDTO.from_cache_entry(entry)
        except CacheMiss:
            pass
        
        # if not in cache -> db
        async with self.uow as uow:
            link = await uow.link_repo.get_by_short(Short(short))
            link.consume_redirect() #metadata.to_vo_container()
            await uow.link_repo.update(link)

        # adding to cache new entry
        entry = LinkCacheEntry.from_entity(link)
        await self.link_cache.save(entry)
        
        return SimpleLinkDTO.from_entity(link)