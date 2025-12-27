from abc import ABC, abstractmethod

from infrastructure.repositories.postgresql.uow import PostgresAuthUoW

from usecase.token.utils.dto import TokenDTO
from usecase.auth.utils.dto import LoginUserDTO

from domain.token.entity import Token
from domain.value_objects.user import Email
from domain.user.exceptions import PasswordMismatchException


class AbstractLoginUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: LoginUserDTO
    ) -> TokenDTO:
        raise NotImplementedError


class PostgresLoginUseCase(AbstractLoginUseCase):
    def __init__(self, uow: PostgresAuthUoW):
        self.uow = uow

    async def execute(
        self,
        dto: LoginUserDTO
    ) -> TokenDTO:
        async with self.uow as uow:
            user_entity = await uow.user_repository.get_by_email(Email(dto.email)) # type: ignore

            if not user_entity.check_password(dto.password):
                raise PasswordMismatchException(user_entity.user_id.value)
            
            token_entity = await uow.token_repository.get_latest_for_user(user_entity.user_id) # type: ignore
            if token_entity is not None:
                token_entity.drop()
                dropped_token = await uow.token_repository.update(token_entity) # type: ignore
            
            created_token = Token.create(user_id=user_entity.user_id)
            new_token_entity = await uow.token_repository.create(entity=created_token) # type: ignore
            return TokenDTO.from_entity(new_token_entity)