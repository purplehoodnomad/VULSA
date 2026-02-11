from infrastructure.uow.link import AbstractLinkUnitOfWork
from domain.link.cache import AbstractLinkCache
from usecase.common.actor import Actor
from domain.value_objects.common import UserId
from domain.value_objects.link import Short, AnonymousEditKey

from .abstract import AbstractDeleteShortUseCase



class DeleteShortUseCase(AbstractDeleteShortUseCase):
    def __init__(
        self,
        uow: AbstractLinkUnitOfWork,
        link_cache: AbstractLinkCache
    ):
        self.uow = uow
        self.link_cache = link_cache

    async def execute(
        self,
        *,
        actor: Actor,
        short: str
    ) -> None:
        async with self.uow as uow:
            if actor.is_user():
                user = await uow.user_repo.get(UserId(actor.id))
                link = await uow.link_repo.get_by_short(Short(short))
                user.validate_link_ownership(link)
            
            if actor.is_anonymous():
                link = await uow.link_repo.get_by_edit_key(AnonymousEditKey(actor.id))
            
            await uow.link_repo.delete(link)
        await self.link_cache.remove(link.short.value)