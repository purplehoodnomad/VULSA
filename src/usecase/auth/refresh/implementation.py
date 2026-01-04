from infrastructure.uow.auth import AbstractAuthUnitOfWork

from domain.value_objects.token import TokenVO
from usecase.auth.utils.dto import TokenDTO

from .abstract import AbstractRefreshAccessTokenUseCase


class PostgresRefreshAccessTokenUseCase(AbstractRefreshAccessTokenUseCase):
    def __init__(self, uow: AbstractAuthUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        refresh_token: str
    ) -> TokenDTO:
        async with self.uow as uow:
            token_entity = await uow.token_repo.get_by_refresh_token(TokenVO(refresh_token)) # type: ignore

            token_entity.refresh()
            
            refreshed_token_entity = await uow.token_repo.update(token_entity) # type: ignore
            return TokenDTO.from_entity(refreshed_token_entity)