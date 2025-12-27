from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgresAuthUoW

from domain.value_objects.token import Token as TokenVO
from domain.token.exceptions import RefreshTokenExpiredException
from usecase.token.utils.dto import TokenDTO


class AbstractRefreshAccessTokenUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        access_token: TokenVO
    ) -> TokenDTO:
        raise NotImplementedError


class PostgresRefreshAccessTokenUseCase(AbstractRefreshAccessTokenUseCase):
    def __init__(self, uow: PostgresAuthUoW):
        self.uow = uow

    async def execute(
        self,
        refresh_token: TokenVO
    ) -> TokenDTO:
        async with self.uow as uow:
            token_entity = await uow.token_repository.get_by_refresh_token(refresh_token) # type: ignore

            token_entity.refresh()
            
            refreshed_token_entity = await uow.token_repository.update(token_entity) # type: ignore
            return TokenDTO.from_entity(refreshed_token_entity)