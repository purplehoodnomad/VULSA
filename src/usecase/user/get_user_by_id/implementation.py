from uuid import UUID

from infrastructure.uow.user import AbstractUserUnitOfWork

from domain.value_objects.common import UserId

from usecase.user.utils.dto import UserDTO

from .abstract import AbstractGetUserByIdUseCase


class PostgresGetUserByIdUseCase(AbstractGetUserByIdUseCase):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: UUID
    ) -> UserDTO:
        async with self.uow as uow:
            user = await uow.user_repo.get(UserId(user_id)) # type: ignore
            
            return UserDTO.from_entity(user)