from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.postgresql.uow.uow import PostgreSQLTokenUoW
from domain.token.entity import Token
from domain.value_objects.common import UserId
from .utils.dto import TokenDTO


class AbstractCreateTokenUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        user_id: UUID
    ) -> TokenDTO:
        raise NotImplementedError


class CreateUserUseCasePostgreSQL(AbstractCreateTokenUseCase):
    def __init__(self, uow: PostgreSQLTokenUoW):
        self.uow = uow

    async def execute(
        self,
        user_id: UUID
    ) -> TokenDTO:
        async with self.uow as uow:
            user_entity = await uow.user_repository.get(UserId(user_id)) # type: ignore

            new_token = Token.create(user_id=user_entity.user_id)
            token_entity = await uow.repository.create(new_token) # type: ignore
            
            return TokenDTO.from_entity(token_entity)