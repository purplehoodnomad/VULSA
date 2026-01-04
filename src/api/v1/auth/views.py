from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from usecase.auth import AbstractRefreshAccessTokenUseCase, AbstractLoginUseCase
from usecase.auth.utils.dto import LoginUserDTO

from .dependencies import get_refresh_access_token_usecase, get_login_usecase
from .schemas import TokenSchema, LoginUserSchema
from .mappers import dto_to_schema


router = APIRouter(prefix="/auth")


@router.post("/refresh", response_model=TokenSchema)
async def refresh_access_token(
    refresh_token: str,
    usecase: AbstractRefreshAccessTokenUseCase = Depends(get_refresh_access_token_usecase)
) -> JSONResponse:
    new_token = await usecase.execute(refresh_token)

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

    tokens = await usecase.execute(dto)
 
    schema = dto_to_schema(tokens)
    return JSONResponse(content=schema.model_dump(mode="json"), status_code=status.HTTP_200_OK)