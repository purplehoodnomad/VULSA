from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from domain.token.exceptions import RefreshTokenExpiredException, TokenDoesNotExistException
from domain.user.exceptions import EmailDoesNotExistException
from domain.value_objects.token import Token as TokenVO

from usecase.auth import AbstractRefreshAccessTokenUseCase, AbstractLoginUseCase
from usecase.auth.utils.dto import LoginUserDTO

from .dependencies import get_refresh_access_token_usecase, get_login_usecase
from .schemas import TokenSchema, LoginUserSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/auth")

security = HTTPBearer(scheme_name="refresh")

@router.post("/refresh", response_model=TokenSchema)
async def refresh_access_token(
    refresh_token: str,
    usecase: AbstractRefreshAccessTokenUseCase = Depends(get_refresh_access_token_usecase)
) -> JSONResponse:
    try:
        new_token = await usecase.execute(TokenVO(refresh_token))
    except RefreshTokenExpiredException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_401_UNAUTHORIZED)
    except TokenDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_401_UNAUTHORIZED)


    schema = dto_to_schema(new_token)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)


@router.post("/login", response_model=TokenSchema)
async def login(
    payload: LoginUserSchema,
    usecase: AbstractLoginUseCase = Depends(get_login_usecase)
) -> JSONResponse:
    
    dto = LoginUserDTO(
        email=payload.email,
        password=payload.password
    )

    try:    
        tokens = await usecase.execute(dto)
    except EmailDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)

    schema = dto_to_schema(tokens)

    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)