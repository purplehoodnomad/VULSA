from abc import ABC

from domain.repositories.abstract import AbstractRepository
from domain.token.entity import Token
from domain.value_objects.token import TokenId, Token as TokenVO


class AbstractTokenRepository(AbstractRepository[Token, TokenId], ABC):
    async def get_by_access_token(self, access_token: TokenVO) -> Token:
        raise NotImplementedError