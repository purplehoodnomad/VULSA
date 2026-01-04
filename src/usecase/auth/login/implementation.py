from infrastructure.uow.auth import AbstractAuthUnitOfWork

from usecase.auth.utils.dto import LoginUserDTO, TokenDTO

from domain.token.entity import Token
from domain.value_objects.user import Email

from .abstract import AbstractLoginUseCase


class PostgresLoginUseCase(AbstractLoginUseCase):
    def __init__(self, uow: AbstractAuthUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        dto: LoginUserDTO
    ) -> TokenDTO:
        async with self.uow as uow:
            user_entity = await uow.user_repo.get_by_email(Email(dto.email))

            user_entity.validate_password(dto.password)
            
            token_entity = await uow.token_repo.get_latest_for_user(user_entity.user_id)
            if token_entity is not None:
                token_entity.drop()
                dropped_token = await uow.token_repo.update(token_entity)
            
            created_token = Token.create(user_id=user_entity.user_id)
            new_token_entity = await uow.token_repo.create(entity=created_token)
            return TokenDTO.from_entity(new_token_entity)