from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from domain.value_objects.common import UserId
from domain.value_objects.user import Email

from usecase.user.utils.dto import UserDeleteDTO


class AbstractDeleteUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserDeleteDTO
    ) -> None:
        raise NotImplementedError


class DeleteUserUseCasePostgreSQL(AbstractDeleteUserUseCase):
    def __init__(self, uow: PostgreSQLUserUoW):
        self.uow = uow

    async def execute(
        self,
        dto: UserDeleteDTO
    ) -> None:
        async with self.uow as uow:
            user = await uow.repository.get(UserId(dto.user_id)) # type: ignore

            if not user.check_password(dto.password):
                raise ValueError("User password mismatch")
            if not user.email == Email(dto.email):
                raise ValueError("User email mismatch")

            await uow.repository.delete(UserId(dto.user_id)) # type: ignore