from infrastructure.uow.user import AbstractUserUnitOfWork

from usecase.user.utils.dto import UserDTO, UserCreateDTO

from .abstract import AbstractCreateUserUseCase


class PostgresCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserDTO:
        async with self.uow as uow:

            entity = dto.to_entity()
            entity.change_password(dto.password)
            
            created_user = await uow.user_repo.create(entity) # type: ignore
            return UserDTO.from_entity(created_user)