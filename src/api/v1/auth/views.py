from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from usecase.auth import AbstractRefreshAccessTokenUseCase, AbstractLoginUseCase
from usecase.auth.utils.dto import LoginUserDTO

from .dependencies import get_refresh_access_token_usecase, get_login_usecase
from .schemas import TokenSchema, LoginUserSchema


router = APIRouter(prefix="/auth")


@router.post("/refresh", response_model=TokenSchema)
async def refresh_access_token(
    refresh_token: str,
    usecase: AbstractRefreshAccessTokenUseCase = Depends(get_refresh_access_token_usecase)
) -> JSONResponse:
    new_token = await usecase.execute(refresh_token)

    return JSONResponse(
        content=new_token.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )


@router.post("/login", response_model=TokenSchema)
async def login(
    payload: LoginUserSchema,
    usecase: AbstractLoginUseCase = Depends(get_login_usecase)
) -> JSONResponse:
    dto = LoginUserDTO.from_schema(payload)
    tokens = await usecase.execute(dto)

    return JSONResponse(
        content=tokens.to_schema().model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )