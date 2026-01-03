from abc import ABC, abstractmethod

from infrastructure.postgresql.uow.uow import PostgresAuthUoW

from domain.value_objects.token import Token as TokenVO
from domain.token.exceptions import AccessTokenExpiredException
from .utils.dto import UserDTO


class AbstractMeUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        access_token: TokenVO
    ) -> UserDTO:
        raise NotImplementedError


class MeUseCasePostgreSQL(AbstractMeUseCase):
    def __init__(self, uow: PostgresAuthUoW):
        self.uow = uow

    async def execute(
        self,
        access_token: TokenVO
    ) -> UserDTO:
        async with self.uow as uow:
            token_entity = await uow.token_repository.get_by_access_token(access_token) # type: ignore
            if not token_entity.is_access_token_valid():
                raise AccessTokenExpiredException(token_entity.access_token.value)
            user_entity = await uow.user_repository.get(token_entity.user_id) # type: ignore

            return UserDTO.from_entity(user_entity)