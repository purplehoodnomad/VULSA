from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from .utils.dto import UserDTO, UserCreateDTO


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserDTO:
        raise NotImplementedError


class CreateUserUseCasePostgreSQL(AbstractCreateUserUseCase):
    def __init__(self, uow: PostgreSQLUserUoW):
        self.uow = uow

    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserDTO:
        async with self.uow as uow:

            entity = dto.to_entity()
            entity.set_password(dto.password)
            
            created_user = await uow.repository.create(entity) # type: ignore
            return UserDTO.from_entity(created_user)