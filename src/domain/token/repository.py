from abc import ABC, abstractmethod

from domain.repositories.abstract import AbstractRepository
from domain.token.entity import Token
from domain.value_objects.token import TokenVO
from domain.value_objects.common import UserId


class AbstractTokenRepository(AbstractRepository[Token], ABC):
    @abstractmethod
    async def get_by_access_token(self, access_token: TokenVO) -> Token:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_refresh_token(self, refresh_token: TokenVO) -> Token:
        raise NotImplementedError
    
    @abstractmethod
    async def get_latest_for_user(self, user_id: UserId) -> Token | None:
        raise NotImplementedError