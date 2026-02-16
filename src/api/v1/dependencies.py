from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from usecase.common.actor import Actor, ActorType
from domain.value_objects.token import TokenVO

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.builders import get_link_uow
from api.v1.user.dependencies import get_get_current_user_usecase

from usecase.user.get_current_user.abstract import AbstractGetCurrentUserUseCase
from usecase.link.get_anonymous_link.abstract import AbstractGetAnonymousLinkUseCase
from usecase.link.get_anonymous_link.implementation import GetAnonymousLinkUseCase



def get_get_anonymous_link_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetAnonymousLinkUseCase:
    uow = get_link_uow(session)
    return GetAnonymousLinkUseCase(uow=uow)


auth = HTTPBearer(auto_error=False)
anon = APIKeyHeader(name="X-Edit-Key", auto_error=False)


async def get_actor(
    edit_key: str | None = Depends(anon),
    credentials: HTTPAuthorizationCredentials | None = Depends(auth),
    user_usecase: AbstractGetCurrentUserUseCase = Depends(get_get_current_user_usecase),
    anonymous_usecase: AbstractGetAnonymousLinkUseCase = Depends(get_get_anonymous_link_usecase),
) -> Actor:

    if credentials is not None:
        access_token = credentials.credentials
        dto = await user_usecase.execute(access_token=TokenVO(value=access_token))
        
        return Actor(id=dto.user_id, type=ActorType.USER)

    if edit_key is not None:
        dto = await anonymous_usecase.execute(edit_key)

        return Actor(id=dto.owner_id, type=ActorType.ANONYMOUS)

    return Actor(id=None, type=ActorType.UNAUTHORIZED)