from infrastructure.uow.link import AbstractLinkUnitOfWork
from usecase.link.utils.dto import LinkStatsDTO
from .abstract import AbstractGetLinkStatsUseCase
from domain.value_objects.link import Short, AnonymousEditKey
from usecase.common.actor import Actor
from domain.value_objects.common import UserId


class GetLinkStatsUseCase(AbstractGetLinkStatsUseCase):
    def __init__(self, uow: AbstractLinkUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        actor: Actor,
        short: str
    ) -> LinkStatsDTO:
        async with self.uow as uow:
            if actor.is_user():
                user = await uow.user_repo.get(UserId(actor.id)) # type: ignore
                link = await uow.link_repo.get_by_short(Short(short))
                user.validate_link_ownership(link)
            
            if actor.is_anonymous():
                link = await uow.link_repo.get_by_edit_key(AnonymousEditKey(actor.id)) # type: ignore
        
                time_stats = await uow.click_repo.get_link_stats_by_time(link)
                geo_stats = await uow.click_repo.get_link_stats_by_geo(link)
                client_stats = await uow.click_repo.get_link_stats_by_client(link)
        
        return LinkStatsDTO.create(link, time_stats, geo_stats, client_stats)