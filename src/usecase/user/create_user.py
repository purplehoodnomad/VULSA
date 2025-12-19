from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from domain.user.entity import User
from domain.value_objects.user import Email, HashedPassword

from usecase.common.mappers import user_entity_to_schema
from usecase.common.dto import UserCreateDTO
from api.v1.user.schemas import UserSchema


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserSchema:
        raise NotImplementedError


class CreateUserUseCasePostgreSQL(AbstractCreateUserUseCase):
    def __init__(self, uow: PostgreSQLUserUoW):
        self.uow = uow

    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserSchema:
        async with self.uow as uow:

            entity = User.create(
                email=Email(dto.email),
                hashed_password=HashedPassword(""),
                status=dto.status
            )
            entity.set_password(dto.password)
            
            output = await uow.repository.create(entity)
            return user_entity_to_schema(output)