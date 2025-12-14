from abc import ABC, abstractmethod

from argon2 import PasswordHasher

from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from domain.user.entity import User
from domain.common.value_objects import UserId
from domain.user.value_objects import Email, HashedPassword

from ..common.mappers import user_entity_to_schema
from ..common.dto import UserCreateDTO
from api.v1.user.schemas import UserSchema


class CreateUserUsecase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserSchema:
        raise NotImplementedError


class CreateUserUsecaseImpl(CreateUserUsecase):
    def __init__(self, uow: PostgreSQLUserUoW):
        self.uow = uow

    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserSchema:
        async with self.uow as uow:
            ph = PasswordHasher()
            hashed = ph.hash(dto.password)

            entity = User.create(
                email=Email(dto.email),
                hashed_password=HashedPassword(hashed),
                status=dto.status
            )
            if uow.repository is not None:
                output = await uow.repository.create(entity)
                return user_entity_to_schema(output)
            
            raise Exception("No repository for UoW")