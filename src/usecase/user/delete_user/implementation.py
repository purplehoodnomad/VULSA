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
            user = await uow.user_repo.get(UserId(dto.user_id))

            user.validate_password(dto.password)
            user.validate_email(Email(dto.email))

            await uow.user_repo.delete(user)