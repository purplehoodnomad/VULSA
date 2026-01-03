from infrastructure.uow.user import AbstractUserUnitOfWork

from domain.value_objects.common import UserId
from domain.value_objects.user import Email

from usecase.user.utils.dto import UserDeleteDTO

from .abstract import AbstractDeleteUserUseCase


class PostgresDeleteUserUseCase(AbstractDeleteUserUseCase):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        dto: UserDeleteDTO
    ) -> None:
        async with self.uow as uow:
            user = await uow.user_repo.get(UserId(dto.user_id)) # type: ignore

            if not user.check_password(dto.password):
                raise ValueError("User password mismatch")
            if not user.email == Email(dto.email):
                raise ValueError("User email mismatch")

            await uow.user_repo.delete(UserId(dto.user_id)) # type: ignore