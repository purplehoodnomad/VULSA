from infrastructure.uow.user import AbstractUserUnitOfWork

from usecase.user.utils.dto import UserDTO, UserCreateDTO

from .abstract import AbstractCreateUserUseCase

from domain.user.entity import User
from domain.value_objects.user import Email, HashedPassword
from domain.value_objects.role import RoleName


class CreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserDTO:
        async with self.uow as uow:
            role_entity = await self.uow.role_repo.get(RoleName(dto.role))
            
            user_entity = User.create(
                email=Email(dto.email),
                hashed_password=HashedPassword(""),
                role=role_entity.name
            )
            user_entity.change_password(dto.password)
            await uow.user_repo.create(user_entity)

            return UserDTO.from_entity(user_entity)