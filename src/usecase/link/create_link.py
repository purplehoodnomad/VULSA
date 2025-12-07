from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from domain.link.entity import Link
from domain.common.value_objects import UserId, LinkId
from domain.link.value_objects import Long, Short, RedirectLimit

from .mappers import to_schema
from .dto import LinkCreateDTO
from api.v1.link.schemas import LinkSchema


class CreateLinkUsecase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkSchema:
        raise NotImplementedError


class CreateLinkUsecaseImpl(CreateLinkUsecase):
    def __init__(self, uow: PostgreSQLLinkUoW):
        self.uow = uow

    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkSchema:
        async with self.uow as uow:
            entity = Link.create(
                user_id=UserId(dto.user_id),
                long=Long(dto.long),
                short=Short(dto.short) if dto.short is not None else None,
                redirect_limit=RedirectLimit(dto.redirect_limit) if dto.redirect_limit is not None else None,
                expires_at=dto.expires_at
            )
            if uow.repository is not None:
                link = await uow.repository.create(entity)
                return to_schema(link)
            
            raise Exception("No repository for UoW")