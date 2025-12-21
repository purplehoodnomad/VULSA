from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from domain.value_objects.common import UserId
from .utils.dto import UserDTO


class AbstractGetUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        user_id: UserId
    ) -> UserDTO:
        raise NotImplementedError


class GetUserUseCasePostgreSQL(AbstractGetUserUseCase):
    def __init__(self, uow: PostgreSQLUserUoW):
        self.uow = uow

    async def execute(
        self,
        user_id: UserId
    ) -> UserDTO:
        async with self.uow as uow:
            user = await uow.repository.get(user_id) # type: ignore
            
            return UserDTO.from_entity(user)