from infrastructure.uow.auth import AbstractAuthUnitOfWork

from domain.value_objects.token import TokenVO
from usecase.user.utils.dto import UserDTO

from .abstract import AbstractGetCurrentUserUseCase


class PostgresGetCurrentUserUseCase(AbstractGetCurrentUserUseCase):
    def __init__(self, uow: AbstractAuthUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        access_token: TokenVO
    ) -> UserDTO:
        async with self.uow as uow:
            token_entity = await uow.token_repo.get_by_access_token(access_token)
            token_entity.validate_access_token()

            user_entity = await uow.user_repo.get(token_entity.user_id)
            return UserDTO.from_entity(user_entity)