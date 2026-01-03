from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgresql.models import TokenORM
from infrastructure.postgresql.exceptions import handle_unique_integrity_error

from domain.token.repository import AbstractTokenRepository
from domain.token.entity import Token
from domain.token.exceptions import TokenDoesNotExistException
from domain.user.entity import User
from domain.value_objects.token import Token as TokenVO
from domain.value_objects.common import UserId


class PostgresTokenRepository(AbstractTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: Token) -> Token:
        token_orm = TokenORM.from_entity(entity)

        self._session.add(token_orm)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e, entity=entity)
        
        return token_orm.to_entity()


    async def update(self, entity: Token) -> Token:
        token_orm = await self._session.get(TokenORM, entity.token_id.value)
        if token_orm is None:
            raise TokenDoesNotExistException(token_id=entity.token_id.value)

        token_orm.access_token = entity.access_token.value
        token_orm.access_token_expires_at = entity.access_token_expires_at
        token_orm.refresh_token = entity.refresh_token.value
        token_orm.refresh_token_expires_at = entity.refresh_token_expires_at

        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e, entity=entity)

        return token_orm.to_entity()


    async def get_latest_for_user(self, user_id: UserId) -> Token | None:
        stmt = select(TokenORM).where(TokenORM.user_id == user_id.value).order_by(TokenORM.refresh_token_expires_at.desc()).limit(1)
        result = await self._session.execute(stmt)
        
        token_orm = result.scalar_one_or_none()
        if token_orm is None:
            return None
        
        return token_orm.to_entity()


    async def get_by_access_token(self, access_token: TokenVO) -> Token:
        stmt = select(TokenORM).where(TokenORM.access_token == access_token.value)
        result = await self._session.execute(stmt)
        
        token_orm = result.scalar_one_or_none()
        if token_orm is None:
            raise TokenDoesNotExistException(access_token=access_token.value)

        return token_orm.to_entity()


    async def get_by_refresh_token(self, refresh_token: TokenVO) -> Token:
        stmt = select(TokenORM).where(TokenORM.refresh_token == refresh_token.value)
        result = await self._session.execute(stmt)
        
        token_orm = result.scalar_one_or_none()
        if token_orm is None:
            raise TokenDoesNotExistException(refresh_token=refresh_token.value)

        return token_orm.to_entity()
