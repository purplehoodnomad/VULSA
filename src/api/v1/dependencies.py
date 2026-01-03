from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.value_objects.token import Token as TokenVO
from domain.token.exceptions import AccessTokenExpiredException, TokenDoesNotExistException

from api.v1.user.dependencies import get_get_current_user_usecase
from usecase.user.get_current_user.abstract import AbstractGetCurrentUserUseCase


security_http_bearer_schema = HTTPBearer(scheme_name="Bearer", description="Access token")


async def get_authentificated_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(security_http_bearer_schema),
        usecase: AbstractGetCurrentUserUseCase = Depends(get_get_current_user_usecase)
    ) -> UUID:
        access_token = credentials.credentials
        try:
            user_dto = await usecase.execute(access_token=TokenVO(access_token))
        except (TokenDoesNotExistException, AccessTokenExpiredException) as e:
            raise HTTPException(detail=e.msg, status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_dto.user_id